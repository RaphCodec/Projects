$path = "C:\Users\rapha\Documents\github\Projects\FireIncidents"
$scriptName = "FireETL.py"

if ( -not (Test-Path -path $path)){
    throw "path does not exist '$path'"
}

cd $path

if ( -not (  "env/" | Test-Path)){
    echo "creating python virtual environment"
    python -m venv env
}

env/Scripts/Activate.ps1

echo "installing dependecies"
pip install -r pydepens.txt


python $scriptName

if ($LASTEXITCODE -ne 0){
    deactivate
    throw "python script failed"
}
deactivate