import numpy as np
from matplotlib import pyplot as pl, lines
import matplotlib
import pylab
import pickle
import scipy
import scipy.stats
import pandas as pd

CTL = 1
AD = 2

markerSize = 60
col1 = 'b'
col2 = 'r'
modelCol = 'g'
# diagCols = {CTL : col2, AD : col1}
trajCol = (0.8, 0, 0.8) # orange
lw = 3  # line width

matplotlib.rcParams.update({'font.size': 16})

np.random.seed(3)

# matplotlib.rc('font', **font)

def adjustFig(maxSize = (600, 400)):
  mng = pl.get_current_fig_manager()
  mng.resize(*maxSize)
  pl.gcf().subplots_adjust(bottom = 0.15)

def plotHist(params1, params2, dist1Rnd, dist2Rnd, dist1Pdf, dist2Pdf):

  fig = pl.figure(1)
  pl.clf()

  xs1 = dist1Rnd(params1[0], params1[1],params1[2])
  xs2 = dist2Rnd(params2[0], params2[1],params2[2])

  xs = np.concatenate((xs1, xs2), axis=0)
  # groupLabels = np.concatenate((np.zeros(xs1.shape), np.ones(xs2.shape)),axis=0)
  #
  # df = pd.DataFrame({'xs': xs, 'type': groupLabels})
  # df['dummy'] = 1
  # ag = df.groupby(['value', 'type']).sum().unstack()
  # ag.columns = ag.columns.droplevel()

  pl.hist(xs1, label='normal', alpha = 0.5, color=col1)
  pl.hist(xs2, label='abnormal', alpha = 0.5, color=col2)

  minX = np.min(xs)
  maxX = np.max(xs)
  scalingFactorPdf = 0.55*params1[2]
  xsDist = np.linspace(minX, maxX, num=100)
  ysDist1 = scalingFactorPdf * dist1Pdf(xsDist, loc=params1[0], scale=params1[1])
  ysDist2 = scalingFactorPdf * dist2Pdf(xsDist, loc=params2[0], scale=params2[1])
  pl.plot(xsDist, ysDist1, linewidth=2, c=col1)
  pl.plot(xsDist, ysDist2, linewidth=2, c=col2)


  pl.plot()

  pl.legend(ncol=2, loc='upper center')
  pl.ylabel('Frequency')
  pl.xlabel('Biomarker Value')
  ax = pl.gca()
  yLim = ax.get_ylim()
  pl.ylim([yLim[0],yLim[1]+0.2*(yLim[1]-yLim[0])])
  pl.xticks([])
  pl.yticks([])
  # pl.xlim(ageLim + np.array([-0.25, 0.25]))

  adjustFig()

  fig.show()

  return fig

def plotHistNoData(params1, params2, dist1Rnd, dist2Rnd, dist1Pdf, dist2Pdf):

  fig = pl.figure(1)
  pl.clf()

  # matplotlib.rcParams['lines.linewidth'] = 20

  xs1 = dist1Rnd(params1[0], params1[1],params1[2])
  xs2 = dist2Rnd(params2[0], params2[1],params2[2])

  xs = np.concatenate((xs1, xs2), axis=0)

  minX = np.min(xs)
  maxX = 0.75*np.max(xs)
  scalingFactorPdf = 0.55*params1[2]
  xsDist = np.linspace(minX, maxX, num=100)
  ysDist1 = scalingFactorPdf * dist1Pdf(xsDist, loc=params1[0], scale=params1[1])
  ysDist2 = scalingFactorPdf * dist2Pdf(xsDist, loc=params2[0], scale=params2[1])
  pl.plot(xsDist, ysDist1, linewidth=2, c=col1)
  pl.plot(xsDist, ysDist2, linewidth=2, c=col2)

  pl.axis('off')

  # rc('lines', linewidth=2, color='r')


  ax = pl.gca()
  yLim = ax.get_ylim()
  pl.ylim([yLim[0],yLim[1]+0.2*(yLim[1]-yLim[0])])
  pl.xticks([])
  pl.yticks([])
  # pl.xlim(ageLim + np.array([-0.25, 0.25]))

  yLimArrow = 0.7*ax.get_ylim()[1]
  delta = 0.45
  ax.annotate(s='', xy=(params1[0]+delta,yLimArrow), xytext=(params2[0]-delta,yLimArrow),
    arrowprops=dict(arrowstyle='<|-|>'))
  ax.text(0.8,20, '>min')
  #ax.arrow(x=params1[0]+delta, y=yLimArrow, dx=(params2[0]-params1[0]-2*delta), dy=0, lw=2)


  adjustFig()

  fig.show()

  return fig


def plotPosVar():

  fig = pl.figure(1)
  pl.clf()
  ax = fig.gca()

  mat = np.array([
    [0.5, 0.1, 0, 0, 0, 0.5],
    [0.5, 0.5, 0, 0, 0, 0],
    [0.0, 0.5, 0.5, 0.1, 0, 0],
    [0.0, 0.0, 0.5, 0.5, 0.1, 0],
    [0.0, 0.0, 0, 0.5, 0.5, 0.1],
    [0.0, 0.0, 0, 0, 0.5, 0.5],
  ])
  ax.imshow(mat, interpolation='nearest', cmap='Greys', vmin=0, vmax=1)

  adjustFig()

  fig.show()

  return fig




paramsFile = 'fig2_params.npz'

dist1Rnd = np.random.normal
dist2Rnd = np.random.normal
dist1Pdf = scipy.stats.norm.pdf
dist2Pdf = scipy.stats.norm.pdf

fig1 = plotHist((0,1,100), (2.5,1,100), dist1Rnd, dist2Rnd, dist1Pdf, dist2Pdf)
fig1.savefig('abnormal1.png', dpi=100)

fig2 = plotHist((0,1,100), (0.3,1,100), dist1Rnd, dist2Rnd, dist1Pdf, dist2Pdf)
fig2.savefig('abnormal2.png', dpi=100)

fig1 = plotHistNoData((0,1,100), (2.5,1,100), dist1Rnd, dist2Rnd, dist1Pdf, dist2Pdf)
fig1.savefig('abnormalNoData.png', dpi=100, bbox_inches='tight')

fig3 = plotPosVar()
fig3.savefig('postvar.png',dpi=100)

dist1Rnd = np.random.normal
# dist2Rnd = np.random.uniform
dist2Rnd = scipy.stats.uniform.rvs
dist1Pdf = scipy.stats.norm.pdf
dist2Pdf = scipy.stats.uniform.pdf

fig1 = plotHist((0,1,100), (-1,5,100), dist1Rnd, dist2Rnd, dist1Pdf, dist2Pdf)
fig1.savefig('abnormalUnif.png', dpi=100)



# dataStruct = dict(figParams=figParams)
# pickle.dump(dataStruct, open(paramsFile,'wb'), protocol=pickle.HIGHEST_PROTOCOL)
