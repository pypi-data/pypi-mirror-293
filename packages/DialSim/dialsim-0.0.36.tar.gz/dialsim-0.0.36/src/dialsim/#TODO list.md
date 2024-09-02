#TODO list
1. Currently Agent uses hard-coded prompt directory for the prompts. Namely, it relies on the files specified on `DialSim` class. This needs to be resolved.
- Maybe upload the predefined .txt files to pypi? And save it in a folder named `prompts`.
2. The exception handling in `load_data` in `DialSim` class is not good. This needs to be resolved. 


###############################
1. num_ret_history adjustment를 어떻게 하면 편하게 할까? -> 현재는 보류 keep as is
2. txt 파일들 open_file하는 방식 --> keep as is
3. stream mode 되는지 보기 (나중에 vllm이랑 연동하면 하는거로)
4.