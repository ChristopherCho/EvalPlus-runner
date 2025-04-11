while getopts "m:n:t:o:" opt; do
    case $opt in
        m) MODEL_PATH=$OPTARG ;;
        n) MODEL_NAME=$OPTARG ;;
        t) TASK=$OPTARG ;;
        o) OUTPUT_DIR=$OPTARG ;;
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

if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR=result/${MODEL_NAME}
    echo "Missing output directory. Set to $OUTPUT_DIR"
fi

if [ -z "$TASK" ]; then
    echo "TASK is not provided. Set to all"
    TASKS=(
        humaneval
        mbpp
    )
else
    TASKS=($TASK)
fi

LOGGING_DIR=${OUTPUT_DIR}/logs
mkdir -p $LOGGING_DIR

evaluate() {
    task=$1
    if [ -f "$OUTPUT_DIR/$task.json" ]; then
        echo "Skipping $task because it already exists"
        return
    fi

    SECONDS=0
    (
        evalplus.evaluate \
            --model $MODEL_PATH \
            --dataset $task \
            --backend vllm \
            --tp 8 \
            --root $LOGGING_DIR \
            --greedy
    ) >$LOGGING_DIR/$task.log
    duration=$SECONDS
    echo "Time taken: $duration seconds" >> $LOGGING_DIR/$task.log

    python get_result.py \
        --task $task \
        --logging_dir $LOGGING_DIR \
        --output_dir $OUTPUT_DIR
}


for task in "${TASKS[@]}"; do
    echo "Evaluating $MODEL_NAME on $task"
    evaluate $task
done
