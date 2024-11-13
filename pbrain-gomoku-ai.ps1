$python_path = (Get-Location).Path + "\src"

$env:PYTHONPATH = $python_path

python -m main $MyInvocation.MyCommand.Path $args
