#!/bin/bash
set -e

# Description:
# Run performance benchmarks using OpenSearch Benchmark
#
# Example:
# ./run-benchmark.sh --endpoint localhost
#
# Usage:
# ./run-benchmark.sh \
#   --endpoint <your endpoint> \
#   --user <username> \
#   --password <password>

# Default values
PORT=80
NUM_RUNS=1
USER=""
PASSWORD=""

# Parse command line arguments
while [ "$1" != "" ]; do
  case $1 in
    -url | --endpoint )    shift
                           ENDPOINT=$1
                           ;;
    -p | --port )          shift
                           PORT=$1
                           ;;
    -n | --num-runs )      shift
                           NUM_RUNS=$1
                           ;;
    -u | --user )          shift
                           USER=$1
                           ;;
    -pwd | --password )    shift
                           PASSWORD=$1
                           ;;
    * )                    echo "Unknown parameter: $1"
                           exit 1
                           ;;
  esac
  shift
done

# Ensure endpoint is specified
if [ -z "$ENDPOINT" ]; then
    echo "--endpoint should be specified"
    exit 1
fi

# Print parameter information
echo "Using endpoint: $ENDPOINT"
echo "Port: $PORT"
echo "Number of runs: $NUM_RUNS"

# Define file and test procedure combinations
declare -a combinations=(
    "./params/filters/efficient/faiss-hnsw-relaxed.json,search-only"
    "./params/filters/efficient/faiss-hnsw-restrictive.json,no-train-test"
    "./params/filters/efficient/faiss-ivf-relaxed.json,train-test"
    "./params/filters/efficient/faiss-ivf-restrictive.json,train-test"
    "./params/filters/efficient/lucene-hnsw-relaxed.json,no-train-test"
    "./params/filters/efficient/lucene-hnsw-restrictive.json,no-train-test"
    "./params/train/train-faiss-sift-128-l2-pq.json,train-test"
    "./params/train/train-faiss-sift-128-l2-sq.json,train-test"
    "./params/train/train-faiss-sift-128-l2.json,train-test"
    "./params/nmslib-sift-128-l2.json,no-train-test"
    "./params/nested/nested-lucene.json,no-train-test"
)

# Create client options if user and password are provided
CLIENT_OPTIONS=""
if [ -n "$USER" ] && [ -n "$PASSWORD" ]; then
    CLIENT_OPTIONS="--client-options=\"basic_auth_user:'$USER',basic_auth_password:'$PASSWORD'\""
    echo "Authentication will be used."
fi

# Execute the benchmark for each combination
for combination in "${combinations[@]}"
do
    # Split the combination into FILE and TEST_PROCEDURE
    IFS=',' read -r FILE TEST_PROCEDURE <<< "$combination"
    
    # Run the benchmark command
    echo "Running benchmark for $FILE with test procedure $TEST_PROCEDURE..."
    command="opensearch-benchmark execute-test --target-hosts $ENDPOINT:$PORT \
        --workload-path ./ \
        --workload-params $FILE \
        --pipeline benchmark-only \
        --kill-running-processes \
        --test-procedure $TEST_PROCEDURE \
        $CLIENT_OPTIONS"
    
    # Execute the command
    eval $command
    
    # Cool down between runs
    sleep 60
done

echo "All benchmarks completed."
