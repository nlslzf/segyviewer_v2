# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 08:41:06 2020

@author: koushb
"""




def do_filter(x):
    file_name=filters.value
    
    data = np.load(file_name, fix_imports=True, encoding='bytes') # array containing dict, dtype 'object'    
    b,a=data['ba']
    for i in range(x.shape[-1]):    
        x[...,i]= lfilter(b, a, x[...,i])
    return(x)


# from https://github.com/geopyteam/cognitivegeo/blob/master/cognitivegeo/src/seismic/attribute.py

def calcEdge_detection(x):
    x=  sobel(x)
    
#    i=att_par.value
#    #['Scipy Sobel','Skimage Sobel','Skimage Roberts','Skimage scharr','Skimage prewitt']
#    if i=='Scipy Sobel':        
#        x = ndimage.sobel(x)
#    elif i=='Skimage Sobel':
#        x=  sobel(x)
#    elif i=='Skimage Roberts':
#        x=  roberts(x)
#    elif i=='Skimage scharr':
#        x=  scharr(x)
#    elif i=='Skimage prewitt':
#        x=  prewitt(x)
#    else:
#        pass
#from skimage.filters import roberts, sobel, sobel_h, sobel_v, scharr, \
#    scharr_h, scharr_v, prewitt, prewitt_v, prewitt_h, farid_v, farid_h

    return(x)

def calcPhaseShift_trace(x,d):
    #from https://stackoverflow.com/questions/52179919/amplitude-and-phase-spectrum-shifting-the-phase-leaving-amplitude-untouched
    
    phase=d*(np.pi/180)
    signalFFT = np.fft.rfft(x)
    

    ## Get Power Spectral Density
    signalPSD = np.abs(signalFFT) ** 2
    signalPSD /= len(signalFFT)**2

    ## Get Phase
    signalPhase = np.angle(signalFFT)

    ## Phase Shift the signal +90 degrees
    newSignalFFT = signalFFT * cmath.rect( 1., phase )

    ## Reverse Fourier transform
    newSignal = np.fft.irfft(newSignalFFT,x.shape[0])
    return newSignal
def calcPhaseShift(x):
    d=att_par.value
    #print(d)
    attrib = x.copy()
    for i in range(x.shape[-1]):    
            attrib[...,i]= calcPhaseShift_trace(x[...,i],d)
    return (attrib)

def calcFirstDerivative_trace(y): #x:time sample y: trace
    x=TimeSamples
    dy = np.zeros(y.shape,np.float)
    dy[0:-1] = np.diff(y)/np.diff(x)
    dy[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
    return(dy)




def calcCumulativeSum(x):
    """
    Calculate cusum attribute
    Args:
        x: seismic data in 3D matrix [Z/XL/IL]
    Return:
        cusum attribute as 3D matrix
    """
    return np.cumsum(x, axis=0)

def calcFirstDerivative(x):
    """
    Calculate first derivative attribute
    Args:
        x: seismic data in 3D matrix [Z/XL/IL]
    Return:
        first-derivative attribute as 3D matrix
    """
    attrib = x.copy()
    for i in range(x.shape[-1]):    
        attrib[...,i]= calcFirstDerivative_trace(x[...,i])
    return attrib

def calcInstanEnvelop(x):
    """
    Calculate instantaneous envelop attribute
    Args:
        x: seismic data in 3D matrix [Z/XL/IL]
    Return:
        Instantaneous envelop attribute as 3D matrix
    """

    attrib = np.abs(hilbert(x, axis=0))

    return attrib

def calcInstanQuadrature(x):
    """
    Calculate instantaneous quadrature attribute
    Args:
        x: seismic data in 3D matrix [Z/XL/IL]
    Return:
        Instantaneous quadrature attribute as 3D matrix
    """

    attrib = np.imag(hilbert(x, axis=0))
    return attrib

def calcInstanPhase(x):
    """
    Calculate instantaneous phase attribute
    Args:
        x: seismic data in 3D matrix [Z/XL/IL]
    Return:
        Instantaneous phase attribute as 3D matrix
    """

    attrib = np.angle(hilbert(x, axis=0))
    attrib = attrib * 180.0 / np.pi
    #
    return attrib

def calcInstanFrequency(x):
    """
    Calculate instantaneous frequency attribute
    Args:
        x: seismic data in 3D matrix [Z/XL/IL]
    Return:
        Instantaneous frequency attribute as 3D matrix
    """

    instphase = np.unwrap(np.angle(hilbert(x, axis=0)), axis=0) * 0.5 / np.pi
    attrib = np.zeros(np.shape(x))
    attrib[1:-1, ...] = 0.5 * (instphase[2:,...] - instphase[0:-2,...])
    return attrib

def calcInstanCosPhase(x):
    """
    Calculate instantaneous cosine of phase attribute
    Args:
        x: seismic data in 3D matrix [Z/XL/IL]
    Return:
        Cosine of phase attribute as 3D matrix
    """

    attrib = np.angle(hilbert(x, axis=0))
    attrib = np.cos(attrib)
    #
    return attrib

def calc_att(x):
    att=attribute.value
    y=x.copy()
    if att=='Phase Shift':
        #print('Phase')
        y=calcPhaseShift(x)
    elif att=='Edge Detection':
        y=calcEdge_detection(x)
    elif att=='CumulativeSum':
        y=calcCumulativeSum(x)
    elif att=='FirstDerivative':
        y=calcFirstDerivative(x)
    elif att=='InstanEnvelop':
        y=calcInstanEnvelop(x)
    elif att=='InstanQuadrature':
        y=calcInstanQuadrature(x)
    elif att=='InstanPhase':
        y=calcInstanPhase(x)
    elif att=='InstanFrequency':
        y=calcInstanFrequency(x)
    elif att=='InstanCosPhase':
        y=calcInstanCosPhase(x)
    return(y)