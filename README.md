# fastapi-vue3-project

## Project initialize
#### 1. Pull whole project form github repository
```sh
# clone remote repository to current folder
git clone https://github.com/windvan/fastapi-vue3-project 

# or to a specific folder
git clone https://github.com/windvan/fastapi-vue3-project local_path
```


#### 2. Initialize frontend
```sh
cd frontend
npm install
```
#### 3. Initialize backend
```sh
cd backend
activate
pip install -r requirements.txt
```
## Environment config
### frontend
- confit backend api base url in `.env.development`
```VITE_API_BASE_URL=http://127.0.0.1:8000```
### backend
- 

## Start dev server
#### 1. backend
```sh
cd backend
activate
cmd:
set ENV=dev (cmd)  or   $env:ENV="dev" (powershell)
python -m app.main   or  python -m uvicorn app.main:app --reload


```
#### 2. frontend
```sh
cd frontend
npm run dev
```


## Rollup and distribute