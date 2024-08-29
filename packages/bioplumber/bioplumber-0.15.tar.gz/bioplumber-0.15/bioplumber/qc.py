import bioplumer.configs as configs


def qc_fastp_(
    read1:str,
    read2:str|None,
    ourdir1:str,
    ourdir2:str|None,
    config:configs.Configs,
    container:str="none",
    **kwargs
    )->str:
    """
    This function ouputs a command to use fastp to quality control fastq files.

    Args:
        read1 (str): The path to the first fastq file
        read2 (str): The path to the second fastq file
        ourdir1 (str): The output directory for the first fastq file
        ourdir2 (str): The output directory for the second fastq file
        container (str): The container to use
        **kwargs: Additional arguments to pass to fastp
    
    """

        
        

