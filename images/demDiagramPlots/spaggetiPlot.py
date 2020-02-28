import numpy as np
from matplotlib import pyplot as pl, lines
import matplotlib
import pylab
import pickle

CTL = 1
AD = 2

markerSize = 60
s1Col = 'r'
s2Col = 'b'
modelCol = 'g'
diagCols = {CTL : s2Col, AD : s1Col}
trajCol = (0, 0, 0) # orange
lw = 3  # line width

matplotlib.rcParams.update({'font.size': 16})


def simpleaxis(ax):
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.get_xaxis().tick_bottom()
  ax.get_yaxis().tick_left()

def plotDPMAndPoints():

  tau = 10 # transition time, use this to find the best b that gives slope a*b/4

  a = 1
  # b = 16/(a*tau)
  c = 4
  d = 5
  fSig = lambda x: a + d/(1+np.exp((-4/tau)*(x-c)))

  xMin = -8
  xMax = 20

  delta = 2
  xs = np.linspace(xMin, xMax, 50)

  fig = pl.figure(1)
  ax = pl.gca()

  pl.plot(xs, fSig(xs), c=trajCol, linewidth=lw, label='Trajectory')

  np.random.seed(2)

  # plot points
  nrSubjLong = 3
  # xsPointsLong = [(xMin + i*start + 1 ) + np.array([0, 3, 6]) for i, start in enumerate([0, 7.5, 9])]
  xsPointsLong = [np.array([-7, -4, -1]), np.array([ 0.5,  3.5, 5,  6.5]), np.array([11, 14, 17])]

  # print(list(enumerate([0, 10, 15])))
  # diag = np.array([1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
  # unqDiags = np.unique(diag)
  # nrDiags = unqDiags.shape[0]
  ysPoints = [fSig(xsPoints) for xsPoints in xsPointsLong]
  ysPointsPerturb = [0 for s in range(nrSubjLong)]
  ysPointsPerturb[0] = ysPoints[0] + 0.4*np.array([-1, 1, -1])
  ysPointsPerturb[1] = ysPoints[1] + 0.4*np.array([1, -1, 1, -1])
  ysPointsPerturb[2] = ysPoints[2] + 0.4*np.array([-1.5, 2, -2])

  print('xsPointsLong', xsPointsLong, 'ysPoints', ysPoints)
  # diagLabels = ['Controls', 'AD Baseline']
  for s in range(nrSubjLong):
    if s == 0:
      label = 'Measurements'
    else:
      label = ''

    pl.plot(xsPointsLong[s], ysPointsPerturb[s], '-',
      linewidth=lw, c='r', label=label)
    pl.scatter(xsPointsLong[s], ysPointsPerturb[s], s=200,marker='.', c='r')

  ax = pl.gca()
  simpleaxis(ax)
  xLim = (xMin, xMax)
  print(xLim)
  yLim = (0, 7)
  xLimShift = 6.7

  # plt.plot(range(5), range(5), 'ro', markersize = 20, clip_on = False, zorder = 100)

  pl.xlim(xLim)
  pl.ylim(yLim)
  pl.legend(ncol=1, loc='lower right')
  pl.xlabel('Disease Stage')
  pl.ylabel('Biomarker Value')
  ax.set_yticklabels(['normal', '', '', '', '', '', '', 'abnormal'])
  ax.set_xticks([])
  yticks = ax.yaxis.get_major_ticks()
  [yticks[i].set_visible(False) for i in range(1,7)]
  # ax.set_yticks([0,7])
  ax.set_xticklabels(['', '', ''])
  pl.gcf().subplots_adjust(left=0.2)
  ax.yaxis.set_label_coords(-0.05, 0.5)

  return fig, xsPointsLong, ysPointsPerturb, xLim


def plotSpaggeti(xsPointsLong, ysPointsPerturb, xLim):

  fig = pl.figure(1)
  pl.clf()
  ax = pl.gca()

  np.random.seed(2)

  # plot points
  nrSubjLong = 3

  xsPointsLong[0] = xsPointsLong[0] -  xsPointsLong[0][0]
  xsPointsLong[1] = xsPointsLong[1] - xsPointsLong[1][0]
  xsPointsLong[2] = xsPointsLong[2] - xsPointsLong[2][0]

  print(xsPointsLong)
  # diagLabels = ['Controls', 'AD Baseline']
  for s in range(nrSubjLong):
    if s == 0:
      label = 'Measurements'
    else:
      label = ''

    pl.plot(xsPointsLong[s], ysPointsPerturb[s], '-',
      linewidth=lw, c='r', label=label)
    pl.scatter(xsPointsLong[s], ysPointsPerturb[s], s = 200, marker = '.', c = 'r')

  ax = pl.gca()
  simpleaxis(ax)
  # xLim = (0, 10)
  xLim = np.array(xLim) - xLim[0]
  print(xLim)
  yLim = (0, 7)

  # plt.plot(range(5), range(5), 'ro', markersize = 20, clip_on = False, zorder = 100)

  pl.xlim(xLim)
  pl.ylim(yLim)
  pl.legend(ncol=1, loc='lower right')
  pl.xlabel('Time Since Baseline')
  pl.ylabel('Biomarker Value')
  ax.set_xticks([])
  yticks = ax.yaxis.get_major_ticks()
  [yticks[i].set_visible(False) for i in range(1, 7)]
  ax.yaxis.set_label_coords(-0.5,1.02)

  ax.set_yticklabels(['normal', '', '', '', '', '', '', 'abnormal'])
  ax.set_xticks(ax.get_xticks()[1:-2])
  ax.set_xticklabels(['', '', ''])
  pl.gcf().subplots_adjust(left=0.2)
  ax.yaxis.set_label_coords(-0.05, 0.5)

  return fig


fig1, xsPointsLong, ysPointsPerturb, xLim = plotDPMAndPoints()
fig1.savefig('spaggeti_fig1.png', dpi=100)

fig2 = plotSpaggeti(xsPointsLong, ysPointsPerturb, xLim)
fig2.savefig('spaggeti_fig2.png', dpi=100)

