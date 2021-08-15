from PIL.PngImagePlugin import PngImageFile, PngInfo
from PIL import Image
from random import randint
import numpy
import sys

def upshift(a,index,n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shiftCol = numpy.roll(col,-n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if(j==index):
                a[i][j] = shiftCol[i]

def downshift(a,index,n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shiftCol = numpy.roll(col,n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if(j==index):
                a[i][j] = shiftCol[i]

def rotate180(n):
    bits = "{0:b}".format(n)
    return int(bits[::-1], 2)


def list_to_str(l:list) -> str:
  return ','.join(map(str, l))

def str_to_list(s:str) -> list:
  return [int(num) for num in s.split(',')]

def read_itxt(file_path:str):
  img = PngImageFile(file_path)
  return img.text

def write_itxt(file_path:str, **kwargs) -> bool:
  try:
    targetImage = PngImageFile(file_path)
  except:
    print('cannot open'+file_path)
    return False
  metadata = PngInfo()
  for key, val in kwargs.items():
    metadata.add_text(key, str(val))
  targetImage.save(file_path, pnginfo=metadata)
  return True

def encode_img(file_name:str):

  input_path = 'input/' + file_name
  output_path = 'encrypted_images/' + file_name

  im = Image.open(input_path)
  pix = im.load()

  #Obtaining the RGB matrices
  r = []
  g = []
  b = []
  for i in range(im.size[0]):
    r.append([])
    g.append([])
    b.append([]) 
    for j in range(im.size[1]):
      rgbPerPixel = pix[i,j]
      r[i].append(rgbPerPixel[0])
      g[i].append(rgbPerPixel[1])
      b[i].append(rgbPerPixel[2])

  m = im.size[0]
  n = im.size[1]

  # Vectors Kr and Kc
  alpha = 8
  Kr = [randint(0,pow(2,alpha)-1) for i in range(m)]
  Kc = [randint(0,pow(2,alpha)-1) for i in range(n)]
  ITER_MAX = 1

  for iterations in range(ITER_MAX):
    # For each row
    for i in range(m):
      rTotalSum = sum(r[i])
      gTotalSum = sum(g[i])
      bTotalSum = sum(b[i])
      rModulus = rTotalSum % 2
      gModulus = gTotalSum % 2
      bModulus = bTotalSum % 2
      if(rModulus==0):
        r[i] = numpy.roll(r[i],Kr[i])
      else:
        r[i] = numpy.roll(r[i],-Kr[i])
      if(gModulus==0):
        g[i] = numpy.roll(g[i],Kr[i])
      else:
        g[i] = numpy.roll(g[i],-Kr[i])
      if(bModulus==0):
        b[i] = numpy.roll(b[i],Kr[i])
      else:
        b[i] = numpy.roll(b[i],-Kr[i])
    # For each column
    for i in range(n):
      rTotalSum = 0
      gTotalSum = 0
      bTotalSum = 0
      for j in range(m):
        rTotalSum += r[j][i]
        gTotalSum += g[j][i]
        bTotalSum += b[j][i]
      rModulus = rTotalSum % 2
      gModulus = gTotalSum % 2
      bModulus = bTotalSum % 2
      if(rModulus==0):
        upshift(r,i,Kc[i])
      else:
        downshift(r,i,Kc[i])
      if(gModulus==0):
        upshift(g,i,Kc[i])
      else:
        downshift(g,i,Kc[i])
      if(bModulus==0):
        upshift(b,i,Kc[i])
      else:
        downshift(b,i,Kc[i])
    # For each row
    for i in range(m):
      for j in range(n):
        if(i%2==1):
          r[i][j] = r[i][j] ^ Kc[j]
          g[i][j] = g[i][j] ^ Kc[j]
          b[i][j] = b[i][j] ^ Kc[j]
        else:
          r[i][j] = r[i][j] ^ rotate180(Kc[j])
          g[i][j] = g[i][j] ^ rotate180(Kc[j])
          b[i][j] = b[i][j] ^ rotate180(Kc[j])
    # For each column
    for j in range(n):
      for i in range(m):
        if(j%2==0):
          r[i][j] = r[i][j] ^ Kr[i]
          g[i][j] = g[i][j] ^ Kr[i]
          b[i][j] = b[i][j] ^ Kr[i]
        else:
          r[i][j] = r[i][j] ^ rotate180(Kr[i])
          g[i][j] = g[i][j] ^ rotate180(Kr[i])
          b[i][j] = b[i][j] ^ rotate180(Kr[i])


  for i in range(m):
    for j in range(n):
      pix[i,j] = (r[i][j],g[i][j],b[i][j])

  im.save(output_path)
  write_itxt(output_path, Kr=list_to_str(Kr), Kc=list_to_str(Kc), ITER_MAX=str(ITER_MAX))


def decode_img(file_name:str):

  input_path = 'encrypted_images/' + file_name
  output_path = 'decrypted_images/' + file_name

  im = Image.open(input_path)
  pix = im.load()


  #Obtaining the RGB matrices
  r = []
  g = []
  b = []
  for i in range(im.size[0]):
    r.append([])
    g.append([])
    b.append([]) 
    for j in range(im.size[1]):
      rgbPerPixel = pix[i,j]
      r[i].append(rgbPerPixel[0])
      g[i].append(rgbPerPixel[1])
      b[i].append(rgbPerPixel[2])

  m = im.size[0]
  n = im.size[1]

  itxt = read_itxt(input_path)
  Kr = str_to_list(itxt['Kr'])
  Kc = str_to_list(itxt['Kc'])
  ITER_MAX = int(itxt['ITER_MAX'])


  for iterations in range(ITER_MAX):
    # For each column
    for j in range(n):
      for i in range(m):
        if(j%2==0):
          r[i][j] = r[i][j] ^ Kr[i]
          g[i][j] = g[i][j] ^ Kr[i]
          b[i][j] = b[i][j] ^ Kr[i]
        else:
          r[i][j] = r[i][j] ^ rotate180(Kr[i])
          g[i][j] = g[i][j] ^ rotate180(Kr[i])
          b[i][j] = b[i][j] ^ rotate180(Kr[i])
    # For each row
    for i in range(m):
      for j in range(n):
        if(i%2==1):
          r[i][j] = r[i][j] ^ Kc[j]
          g[i][j] = g[i][j] ^ Kc[j]
          b[i][j] = b[i][j] ^ Kc[j]
        else:
          r[i][j] = r[i][j] ^ rotate180(Kc[j])
          g[i][j] = g[i][j] ^ rotate180(Kc[j])
          b[i][j] = b[i][j] ^ rotate180(Kc[j])
    # For each column
    for i in range(n):
      rTotalSum = 0
      gTotalSum = 0
      bTotalSum = 0
      for j in range(m):
        rTotalSum += r[j][i]
        gTotalSum += g[j][i]
        bTotalSum += b[j][i]
      rModulus = rTotalSum % 2
      gModulus = gTotalSum % 2
      bModulus = bTotalSum % 2
      if(rModulus==0):
        downshift(r,i,Kc[i])
      else:
        upshift(r,i,Kc[i])
      if(gModulus==0):
        downshift(g,i,Kc[i])
      else:
        upshift(g,i,Kc[i])
      if(bModulus==0):
        downshift(b,i,Kc[i])
      else:
        upshift(b,i,Kc[i])

    # For each row
    for i in range(m):
      rTotalSum = sum(r[i])
      gTotalSum = sum(g[i])
      bTotalSum = sum(b[i])
      rModulus = rTotalSum % 2
      gModulus = gTotalSum % 2
      bModulus = bTotalSum % 2
      if(rModulus==0):
        r[i] = numpy.roll(r[i],-Kr[i])
      else:
        r[i] = numpy.roll(r[i],Kr[i])
      if(gModulus==0):
        g[i] = numpy.roll(g[i],-Kr[i])
      else:
        g[i] = numpy.roll(g[i],Kr[i])
      if(bModulus==0):
        b[i] = numpy.roll(b[i],-Kr[i])
      else:
        b[i] = numpy.roll(b[i],Kr[i])

  for i in range(m):
    for j in range(n):
      pix[i,j] = (r[i][j],g[i][j],b[i][j])

  im.save(output_path)