class FileManager:
    """Handles reading and writing of files."""
    
    @staticmethod
    def read_file(file, mode='r'):
        with open(file, mode) as f:
            return f.read() if 'b' not in mode else f.read()
    
    @staticmethod
    def write_file(file, content):
        with open(file, 'w') as f:
            f.write(content)
