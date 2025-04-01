while getopts "m:n:t:" opt; do
    case $opt in
        m) MODEL_PATH=$OPTARG ;;
        n) MODEL_NAME=$OPTARG ;;
        t) TENSOR_PARALLEL_SIZE=$OPTARG ;;
    esac
done

if [ -z "$MODEL_PATH" ]; then
    echo "Missing model path"
    exit 1
fi

if [ -z "$MODEL_NAME" ]; then
    MODEL_NAME=$(basename $MODEL_PATH)
    echo "Missing model name. Use $MODEL_NAME"
fi

if [ -z "$TENSOR_PARALLEL_SIZE" ]; then
    TENSOR_PARALLEL_SIZE=8
    echo "Missing tensor parallel size. Set to $TENSOR_PARALLEL_SIZE"
fi

output_dir="result/$MODEL_NAME"
logging_dir="result/$MODEL_NAME/logs"
mkdir -p $logging_dir

evaluate() {
    task=$1
    if [ -f "$output_dir/$task.json" ]; then
        echo "Skipping $task because it already exists"
        return
    fi

    SECONDS=0
    (
        evalplus.evaluate \
            --model $MODEL_PATH \
            --dataset $task \
            --backend vllm \
            --tp $TENSOR_PARALLEL_SIZE \
            --root $logging_dir \
            --greedy
    ) >$logging_dir/$task.log
    duration=$SECONDS
    echo "Time taken: $duration seconds" >> $logging_dir/$task.log

    python get_result.py \
        --task $task \
        --logging_dir $logging_dir \
        --output_dir $output_dir
}


tasks=(
    humaneval
    mbpp
)
for task in "${tasks[@]}"; do
    echo "Evaluating $MODEL_NAME on $task"
    evaluate $task
done
