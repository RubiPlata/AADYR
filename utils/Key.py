import os

# =========================
# IMPORTACIÓN SEGURA DE BOTO3
# =========================
try:
    import boto3
    from botocore.exceptions import NoCredentialsError
    AWS_AVAILABLE = True
except ImportError:
    boto3 = None
    AWS_AVAILABLE = False


class Settings:
    """
    Clase para manejar variables de entorno.
    
    - Si AWS está disponible → usa AWS SSM Parameter Store
    - Si NO está disponible → usa variables locales (os.environ)
    """

    def __init__(self, region="us-east-1"):
        self.use_aws = False
        self.ssm = None

        if AWS_AVAILABLE:
            try:
                self.ssm = boto3.client("ssm", region_name=region)
                self.use_aws = True
            except Exception:
                self.use_aws = False

    # =========================
    # SET VARIABLE
    # =========================
    def set(self, key_name, value, secure=True):
        """
        Guarda una variable:
        - En AWS SSM si está disponible
        - En entorno local si no
        """

        if self.use_aws:
            try:
                param_type = "SecureString" if secure else "String"

                return self.ssm.put_parameter(
                    Name=key_name,
                    Value=value,
                    Type=param_type,
                    Overwrite=True
                )

            except Exception as e:
                return {"error": str(e)}

        # Modo local
        os.environ[key_name] = value
        return {"message": "Guardado localmente"}

    # =========================
    # GET VARIABLE
    # =========================
    def get(self, key_name, decrypt=True):
        """
        Obtiene una variable:
        - Desde AWS SSM si está disponible
        - Desde entorno local si no
        """

        if self.use_aws:
            try:
                response = self.ssm.get_parameter(
                    Name=key_name,
                    WithDecryption=decrypt
                )
                return response["Parameter"]["Value"]

            except Exception:
                return None

        # Modo local
        return os.getenv(key_name)