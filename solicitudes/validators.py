from django.core.exceptions import ValidationError
from django.core import validators


def valid_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and 
        not value.name.endswith('.gif') and
        not value.name.endswith('.bmp') and 
        not value.name.endswith('.jpg') and
        not value.name.endswith('.docx') and
        not value.name.endswith('.xlsx') and
        not value.name.endswith('.pdf') and
        not value.name.endswith('.pptx')):
 
        raise ValidationError("Archivos permitidos: .jpg, .jpeg, .png, .gif, .bmp, .docx, .xlsx, .pdf, .pptx")



def validate_file_size(value):
    filesize= value.size
    
    if filesize > 2485760:
        raise ValidationError("El tamaño maximo de archivo permitido es 2MB")
    else:
        return value



def descripcion_validation(value):
    if len(value) > 80:
        raise ValidationError('La descripción debe contener maximo 80 caracteres')



def descripcion_validation_sol(value):
    if len(value) > 500:
        raise ValidationError('La descripción debe contener maximo 500 caracteres')



def is_email(value):
    """
    Returns whether the given value is an e-mail address.
    :return: bool
    """
    try:
        validators.validate_email(value)
        return True
    except validators.ValidationError:
        return False 
