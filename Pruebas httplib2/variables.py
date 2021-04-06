import os
print({k:v for k,v in os.environ.items() if 'proxy' in k.lower()})
