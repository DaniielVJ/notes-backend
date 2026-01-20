# Alias para el comando que instala todas las dependencias especificadas en el requirementst.xt
install:
	pip install -r requirements.txt


# Alias para que el servidor web ejecute la aplicacion creada en fastapi
run-local:
	uvicorn app.main:app --reload

