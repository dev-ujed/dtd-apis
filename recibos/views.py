from django.http.response import HttpResponse
from django.shortcuts import render

from .models import TNArchivo, TNFactura

from PyPDF2 import PdfFileReader, PdfFileWriter
import sys


# Create your views here.
def get_recibos_nomina(request):
    nomina = '01'
    periodo = 'Q202118'
    matricula = '905891'
    archivo_gral = 'PDF_' + periodo + '_' + nomina + '.pdf'

    recibos = list(TNFactura.objects.filter(tfac_estatus='A', tfac_nomina=nomina, tfac_periodo=periodo).order_by('tfac_matricula').values_list('tfac_id', flat=True))
    print(recibos)

    # for element in recibos:
    #     archivo = TNArchivo.objects.get(tarc_id=element)
    #     # print(archivo.tarc_nombre_pdf)
    #     with open(archivo_gral, 'ab') as binary_file:
    #         binary_file.write(archivo.tarc_archivo_pdf)
    #         binary_file.close()

    #     # for line in open(archivo.tarc_nombre_pdf, 'rb').readlines():
    #     #     file.write(line)
    #     # file.close()
    input_streams = []
    try:
        # First open all the files, then produce the output file, and
        # finally close the input files. This is necessary because
        # the data isn't read from the input files until the write
        # operation. Thanks to
        # https://stackoverflow.com/questions/6773631/problem-with-closing-python-pypdf-writing-getting-a-valueerror-i-o-operation/6773733#6773733

        for element in recibos:
            archivo = TNArchivo.objects.get(tarc_id=element)
            input_streams.append(archivo.tarc_archivo_pdf)
        writer = PdfFileWriter()
        for reader in map(PdfFileReader, input_streams):
            for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
        writer.write(archivo_gral)
    finally:
        # for f in input_streams:
        #     f.close()
        # output_stream.close()
        archivo_gral.close()

    print('terminó')
    return HttpResponse('ok')
