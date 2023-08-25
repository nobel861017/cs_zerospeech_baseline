# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import torch
import numpy as np
import time
import argparse
import sys
import os
import json
from random import shuffle
from clustering import kMeanCluster, kMeanGPU_fairseq, kMeanGPU_S3PRL
from pathlib import Path
import fairseq
import yaml
import s3prl.hub as hub

def getQuantile(sortedData, percent):
    return sortedData[int(percent * len(sortedData))]


def parseArgs(argv):
    # Run parameters
    parser = argparse.ArgumentParser(description='Clustering module using kmeans or dpmeans.')
    #parser.add_argument('pathOutput', type=str,
    #                    help="Path to the output clustering checkpoint.")
    parser.add_argument('--config', type=str, default='cluster_config.yaml', help='The path to the config file.')
    
    #parser.add_argument(
    #    '--pathDB', nargs="*", type=str,
    #    default=["/work/b08202033/sWUGGY/datasets/LibriSpeech/train-clean-100/"])
    #parser.add_argument('-k', '--nClusters', type=int, default=50,
    #                    help="Number of clusters for kmeans algorithm (default: 50).")
    #parser.add_argument('-g',  '--nGroups', type=int, default=1,
    #                    help="Number of groups for kmeans algorithm (default: 1).")
    #parser.add_argument('-n', '--MAX_ITER', type=int, default=100,
    #                   help="Number of iterations (default: 100).")
    #parser.add_argument('--recursionLevel', type=int, default=2,
    #                    help="The speaker recursionLevel in the training dataset (default: 2).")
    #parser.add_argument('--extension', nargs='*', type=str, default=['.flac', '.wav'],
    #                    help="The audio file extension (default: .flac).")
    #parser.add_argument('--seqList', type=str, default=None,
    #                    help="Specific the training sequence list (default: None).")
    #parser.add_argument('--sizeWindow', type=int, default=10240,
    #                    help="The size of the window when loading audio data (default: 10240).")
    #parser.add_argument('--debug', action='store_true',
    #                    help='Debug mode, only use a small number of training data.')
    #parser.add_argument('--encoder_layer', action='store_true',
    #                    help='Whether to use the output of the encoder for the clustering.')
    #parser.add_argument('--level_gru', type=int, default=None,
    #                    help='Specify the LSTM hidden level to take the representation (default: None).')
    #parser.add_argument('--batchSizeGPU', type=int, default=50,
    #                    help='Batch size of each GPU (default: 50).')
    #parser.add_argument('--DPMean', action='store_true',
    #                    help='Activate DPMeans training instead of Kmeans.')
    #parser.add_argument('-l', '--DPLambda', type=float, default=11,
    #                    help='Lambda parameter of DPMeans algo (default: 11).')
    #parser.add_argument('--perIterSize', type=int, default=-1,
    #                    help='(Depreciated) Number of items per iteration (default: -1).')
    #parser.add_argument('--train_mode', action='store_true',
    #                    help='Activate training CPC module too.')
    #parser.add_argument('--dimReduction', type=str, default=None,
    #                    help='Dimentionality reduction (default: None)')
    #parser.add_argument('--centroidLimits', type=int, nargs=2, default=None,
    #                    help='centroidLimits when using dimentionality reduction (default: None)')
    #parser.add_argument('--getDistanceEstimation', action='store_true',
    #                    help='Get distance estimation')
    #parser.add_argument('--save', action='store_true',
    #                    help='Save the intermediate checkpoints. The checkpoints will'
    #                    'be saved in the same directory as the output.')
    #parser.add_argument('--load', action='store_true',
    #                    help='Load the last checkpoint from the same directory as the output.')
    #parser.add_argument('--save-last', type=int, default=5,
    #                    help='Number of last checkpoints to be saved (default: 5).')
    #parser.add_argument('--model_type', type=str, default="hubert",
    #                    help='Upstream model from s3prl model list.')
    #parser.add_argument('--cp_path', type=str, default="/work/b08202033/multilingual_zero_resource_challenge/xlsr2_960m_1000k.pt",
    #                    help='Checkpoint path of the multilingual speech foundation model.')
    #parser.add_argument('--epsilon', type=float, default=1e-4)
    return parser.parse_args(argv)


if __name__ == "__main__":
    torch.cuda.empty_cache()

    import os
    #from cpc.feature_loader import loadModel, FeatureModule
    from dataset import findAllSeqs, filterSeqs, AudioBatchData, findAllSeqs_Mix

    args = parseArgs(sys.argv[1:])

    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        print(config)
    
    assert (config['runner']['cp_path'] is None and config['runner']['s3prl'] is not None) \
            or (config['runner']['cp_path'] is not None and config['runner']['s3prl'] is None), \
            "Don't use fairseq model and s3prl model at once."
    # Export absolute paths for later use
    #args.pathOutput = os.path.abspath(args.pathOutput)
    pathOutput = os.path.abspath(config['runner']['pathOutput'])
    
    #assert False==True
    pathDB = config['data']['pathDB']
    for i in range(len(pathDB)):
        pathDB[i] = os.path.abspath(pathDB[i])

    #print(args.pathDB)
    load = config['runner']['load']
    # Now, args.pathDB will be a list
    if not load: 
        assert os.path.exists(pathOutput) is False, \
            f"The output file {pathOutput} already exists, please check the option --load !"
        assert os.path.exists(os.path.join(os.path.dirname(pathOutput), "checkpoint_last.pt")) is False, \
            f"Found last_checkpoint.pt in the output directory, please check the option --load !"
    recursionLevel = config['data']['recursionLevel']
    extension = config['data']['extension']
    seqNames, speakers = findAllSeqs_Mix(pathDB,
                                    speaker_level=recursionLevel,
                                    extension=extension,
                                    loadCache=True)
    seqList = config['data']['seqList']
    if seqList is not None:
        seqNames = filterSeqs(seqList, seqNames)

    debug = config['runner']['debug']
    #print(seqNames)
    #assert False==True
    if debug:
        nsamples = 1000
        print(f"Debug mode activated, get only {nsamples} samples!")
        shuffle(seqNames)
        seqNames = seqNames[:nsamples]
    
    getDistanceEstimation = config['runner']['getDistanceEstimation']
    if getDistanceEstimation:
        shuffle(seqNames)
        seqNames = seqNames[:5000]

    print("")
    print(f'Loading audio data at {pathDB}')
    start_time = time.time()
    sizeWindow = config['data']['sizeWindow']
    dataset = AudioBatchData(pathDB,
                             sizeWindow,
                             seqNames,
                             None,
                             len(speakers))
    print(f"Dataset loaded in {time.time()-start_time} seconds !")
    print("")

    batchSizeGPU = config['data']['batchSizeGPU']
    nGPUs = torch.cuda.device_count()
    batchSize = batchSizeGPU * nGPUs
    trainLoader = dataset.getDataLoader(batchSize, "uniform",
                                        False, numWorkers=16)
    device_ids = list(range(nGPUs))
    print(f"Length of dataLoader: {len(trainLoader)}")
    print("")

    level_gru = config['runner']['level_gru']
    if level_gru is None:
        updateConfig = None
    else:
        updateConfig = argparse.Namespace(nLevelsGRU=level_gru)

    # model = loadModel([args.pathCheckpoint][0], updateConfig=updateConfig)[0]
    # featureMaker = FeatureModule(model, args.encoder_layer)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # featureMaker = getattr(hub, args.model_type)().to(device).eval()
    
    model_name = None
    flag = None
    if config['runner']['cp_path'] is not None:
        cp_path = config['runner']['cp_path']
        flag = 'fairseq'
        model_name = cp_path
        model, cfg, task = fairseq.checkpoint_utils.load_model_ensemble_and_task([cp_path])
        #featureMaker = torch.nn.DataParallel(model[0]).to(device)
        featureMaker = model[0].to(device)

    elif config['runner']['s3prl'] is not None:
        flag = 's3prl'
        model_name = config['runner']['s3prl']
        featureMaker = getattr(hub, config['runner']['s3prl'])().to(device)
    
    else:
        print("Please specify the speech encoder in the config file.")
        raise
    
    featureMaker.eval()
    print(f"Feature maker {model_name} loaded!")
    print("")

    
    if not config['runner']['train_mode']:
        featureMaker.eval()
    featureMaker.cuda()

    # Check if dir exists
    if not os.path.exists(os.path.dirname(pathOutput)) and os.path.dirname(pathOutput):
        Path(os.path.dirname(pathOutput)).mkdir(parents=True, exist_ok=True)

    pathConfig = f"{os.path.splitext(pathOutput)[0]}_args.yaml"
    #with open(pathConfig, 'w') as file:
    #    json.dump(vars(args), file, indent=2)
    with open(pathConfig, 'w') as file:
        documents = yaml.dump(config, file)

    out_state_dict = {}
    print("Starting the clustering...")
    start_time = time.time()

    assert flag in ['fairseq', 's3prl'], "Currently only supported speech encoder from s3prl and fairseq."
    
    if flag == 'fairseq':
        clusters = kMeanGPU_fairseq(trainLoader, featureMaker.eval(), config['runner']['nClusters'], config['runner']['nGroups'],
                                perIterSize=config['runner']['perIterSize'],
                                MAX_ITER=config['runner']['MAX_ITER'],
                                save=config['runner']['save'], load=load, 
                                save_dir=os.path.dirname(pathOutput),
                                save_last=config['runner']['save_last'],
                                EPSILON=config['runner']['epsilon'],
                                device_ids=device_ids,
                                layer=config['runner']['layer']
                                ).cpu()
    
    elif flag == 's3prl':
        clusters = kMeanGPU_S3PRL(trainLoader, featureMaker.eval(), config['runner']['nClusters'], config['runner']['nGroups'],
                                perIterSize=config['runner']['perIterSize'],
                                MAX_ITER=config['runner']['MAX_ITER'],
                                save=config['runner']['save'], load=load, 
                                save_dir=os.path.dirname(pathOutput),
                                save_last=config['runner']['save_last'],
                                EPSILON=config['runner']['epsilon'],
                                layer=config['runner']['layer']
                                ).cpu()
    


    print(f'Ran clustering '
          f'in {time.time() - start_time:.2f} seconds')

    clusterModule = kMeanCluster(clusters)
    out_state_dict["state_dict"] = clusterModule.state_dict()
    out_state_dict["encoder_layer"] = config['runner']['encoder_layer']
    out_state_dict["n_clusters"] = config['runner']['nClusters']
    out_state_dict['dim'] = clusters.size(2)
    torch.save(out_state_dict, pathOutput)
    with open(pathConfig, 'w') as file:
        documents = yaml.dump(config, file)