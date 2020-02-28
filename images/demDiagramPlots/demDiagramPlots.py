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
trajCol = (0.8, 0, 0.8) # orange
lw = 3  # line width

matplotlib.rcParams.update({'font.size': 16})

# matplotlib.rc('font', **font)

def adjustFig(maxSize = (600, 400)):
  mng = pl.get_current_fig_manager()
  mng.resize(*maxSize)
  pl.gcf().subplots_adjust(bottom = 0.15)

def plotLinearRegr():

  fig = pl.figure(1)

  # for two subjects plot 4 biomk measurements each
  ageDeltas = [0,0.4,1.2,1.5]
  ageS1 = np.array(ageDeltas)[[0,3]] #+ 70
  biomkS1 = [6, 5] # [6, 5.1, 5.8, 5]
  ageS2 = np.array(ageDeltas) #+ 70.25
  biomkS2 = [3.5, 4, 2, 2.5]


  pl.scatter(ageS1, biomkS1, s=markerSize,marker='x', c=s2Col, label='Subject 1', linewidths=lw)
  pl.scatter(ageS2, biomkS2, s=markerSize, marker='x', c=s1Col, label='Subject 2', linewidths=lw)

  # fit lines to each subject
  polyCoeff1 = np.polyfit(ageS1, biomkS1, deg=1)
  polyCoeff2 = np.polyfit(ageS2, biomkS2, deg=1)
  ageLim = np.array([np.min([np.min(ageS1), np.min(ageS2)]), np.max([np.max(ageS1), np.max(ageS2)])])
  pl.plot(ageLim, polyCoeff1[0] * ageLim + polyCoeff1[1], c=s2Col, linewidth=lw)
  pl.plot(ageLim, polyCoeff2[0] * ageLim + polyCoeff2[1], c=s1Col, linewidth=lw)

  pl.plot()

  pl.legend(ncol=2, loc='upper center')
  pl.xlabel('Years since baseline')
  pl.ylabel('Biomarker Value')
  pl.xticks(ageS1)
  pl.ylim([1,8])
  pl.xlim(ageLim + np.array([-0.25, 0.25]))

  pl.xticks([0, 0.5, 1, 1.5])

  adjustFig()

  fig.show()

  return fig

def plotGPfit():
  a = 0.5
  b = 2
  c = 1
  sqrtBigD = np.sqrt(b**2 - 4*a*c)
  fQuad = lambda x: a*x**2 + b*x + c
  xSol1 = (-b-sqrtBigD)/(2*a)
  xSol2 = (-b+sqrtBigD)/(2*a)

  uScale = 1.3
  lScale = 0.6
  fUpper = lambda x: uScale * a * x ** 2 + uScale * b * x + (c + 1)
  fLower = lambda x: lScale * a * x ** 2 + lScale * b * x + (c - 1.2)

  print('sqrtBigD', sqrtBigD, 'fQuad(xSol1)', fQuad(xSol1))
  # assert abs(fQuad(xSol1)) < 0.001
  # assert abs(fQuad(xSol2)) < 0.001

  xOuterDelta = (xSol2 - xSol1)/10
  xsModel = np.linspace(xSol1 - xOuterDelta, xSol2 + xOuterDelta, 50)
  ysModel = fQuad(xsModel)
  ysUpper = fUpper(xsModel)
  ysLower = fLower(xsModel)

  fig = pl.figure(2)

  pl.plot(xsModel,ysModel, c=modelCol, linewidth=lw, label='Model Prediction')
  pl.plot(xsModel, ysUpper, '--', c=modelCol, linewidth=lw, label='Confidence Interval')
  pl.plot(xsModel, ysLower, '--', c=modelCol, linewidth=lw)
  nrPoints = 20
  xsPoints = np.linspace(xSol1 - xOuterDelta, xSol2 + xOuterDelta, nrPoints)
  ysPoints = fQuad(xsPoints) + np.random.normal(loc=0, scale=0.27, size=nrPoints)
  pl.scatter(xsPoints, ysPoints, marker='x', s=markerSize, linewidths=lw,
    label='Subject Specific Slopes')
  ax = pl.gca()
  xLim = ax.get_xlim()
  print(xLim)
  pl.plot([xLim[0], xLim[1]], [0,0], '--', c=(0.5,0.5,0.5), linewidth=lw)

  pl.xlim(xLim)
  pl.ylim(-2,3)
  pl.legend(ncol=1, loc='upper center')
  pl.xlabel('Biomarker Value')
  pl.ylabel('Rate of Change')
  ax.set_xticklabels(['0', '2', '4', '6', '', '', '', ''])

  adjustFig()

  fig.show()

  figParams = (xsPoints, ysPoints, xsModel, ysModel, ysUpper, ysLower, xLim)

  return fig, figParams


def plotTrajReconstruction(figParams):
  vertShift = 0.4

  tau = -10 # transition time, use this to find the best b that gives slope a*b/4
  a = 1.2
  # b = 16/(a*tau)
  c = 20
  d = 4.5
  fSig = lambda x: a + d/(1+np.exp((-4/tau)*(x-c)))

  xMin = 0
  xMax = 40

  xOuterDelta = 0
  xs = np.linspace(xMin - xOuterDelta, xMax + xOuterDelta, 50)

  nrVirtualSubfigs = 3
  fig = pl.figure(2)

  ################ make first axes, plot rotated function ##################
  ax0 = pl.subplot2grid((1, nrVirtualSubfigs), (0,0), colspan=1)
  ax0.set_frame_on(False)
  fig.subplots_adjust(top=0.75)

  (xsPoints, ysPoints, xsModel, ysModel, ysUpper, ysLower, xLim) = figParams
  print(xsPoints, ysPoints, xsModel, ysModel, ysUpper, ysLower, xLim)
  # print(adasd)

  legendEntries = []

  # plot 90-degree rotated image by inverting ys with xs
  lhModel =ax0.plot(ysModel, xsModel, c=modelCol, linewidth=lw, label='Model Prediction')
  # legendEntries.append(lhModel)
  ax0.plot(ysUpper, xsModel, '--', c=modelCol, linewidth=lw, alpha=0.4, label='Confidence Interval')
  ax0.plot(ysLower, xsModel, '--', c=modelCol, linewidth=lw, alpha=0.4)
  nrPoints = 20
  ax0.scatter(ysPoints, xsPoints, marker='x', s=markerSize, linewidths=lw,
    label='Subject Measurements')
  ax0.set_xlim((-2,1.3))
  ax0.invert_xaxis()
  yLim0 = xLim # # need xLim as fig is rotated
  # yLim0Delta = 1
  ax0.set_ylim((yLim0[0] - 0, yLim0[1] - 0.1))
  ax0.set_yticks([])
  ax0.set_xticks([1, 0, -1])
  pl.xlabel('Rate of Change')

  pl.plot([0,0], [xLim[0], xLim[1]], '--', c=(0.5,0.5,0.5), linewidth=lw)

  ############ make second axes, plot the function reconstruction #################

  ax1 = pl.subplot2grid((1, nrVirtualSubfigs), (0,1), colspan=(nrVirtualSubfigs-1))
  # pl.gcf().subplots_adjust(left=0.2)
  # ax.set_frame_on(True)

  print(fSig(xs).shape, xs.shape)
  pl.plot(xs,fSig(xs), c=trajCol, linewidth=lw, label='Model Prediction')

  ax1 = pl.gca()
  xLim = ax1.get_xlim()
  print(xLim)
  # pl.plot([xLim[0], xLim[1]], [0,0], '--', c=(0.5,0.5,0.5), linewidth=lw)


  # pl.legend(ncol=1, loc='upper right')
  pl.xlabel('Relative Time (years)')
  pl.ylabel('Biomarker Value')
  ax1.yaxis.set_label_coords(-0.6, 0.5)

  limitColor = (0.8, 0.8, 0)
  slopeLineColor = (0.8, 0, 0)


  ax1.set_xlim(xLim)
  ax1.set_ylim(0 + vertShift,6 + vertShift)
  # ax.set_xticklabels(['', '1', '2', '3', '4', '5', '6', '7'])

  ############## plot guide lines on top of all other subfigures ################

  ax3 = pl.axes([0, 0, 1, 1], facecolor=(1, 1, 1, 0))
  ax3.set_frame_on(False)

  # make the upper and lower integration limits
  ax3.set_xlim((0, 1))
  ax3.set_ylim((0,1))

  deltaL = 0.04
  uL = 0.725 - deltaL# upper integration limit
  lL = 0.26 - deltaL# lower integration  limit
  lrShift = 0
  leftL = 0.215 + lrShift
  lhLimit = ax3.plot([leftL, 0.6], [uL, uL], '--', c=limitColor, linewidth=lw, label='Limit')
  ax3.plot([leftL, 0.8], [lL, lL], '--', c=limitColor, linewidth=lw)
  legendEntries.append(lhLimit)

  # make the line going to the slope
  yRecon = 0.57
  ax3.plot([0.265 + lrShift, 0.62 + lrShift], [yRecon, yRecon], '--', c=slopeLineColor, linewidth=lw)
  lhRecon = ax3.plot([0.62 - 0.03, 0.62 + 0.03], [0.65, 0.50], '-', c=slopeLineColor, linewidth=lw,
    label='Reconstruction')
  legendEntries.append(lhRecon)

  cols = [trajCol, limitColor, slopeLineColor]
  lineStyles = ['-', '--', '-']
  legFigs = [pl.Line2D([0, 0], [0, 1], color=col, linestyle=style, linewidth=lw)
    for col, style in zip(cols, lineStyles)]
  pl.legend(legFigs, ['Integrated Trajectory', 'Integration Limit', 'Slope'], ncol=2,
    loc='upper center')

  # adjustFig((500, 400))
  adjustFig()

  fig.show()

  return fig

def plotTrajAlignment():
  tau = -10 # transition time, use this to find the best b that gives slope a*b/4

  a = 1
  # b = 16/(a*tau)
  c = 4
  d = 5
  fSig = lambda x: a + d/(1+np.exp((-4/tau)*(x-c)))

  xMin = -12
  xMax = 25

  delta = 5
  xs = np.linspace(xMin, xMax, 50)

  fig = pl.figure(2, figsize = (6,4))
  ax = pl.subplot(111)
  ax.set_frame_on(True)
  fig.subplots_adjust(top=0.75)

  # plot trajectory
  ax.plot(xs,fSig(xs), c=trajCol, linewidth=lw, label='Trajectory')

  np.random.seed(2)

  # plot points
  nrPoints = 19
  xsPoints = np.array([-10, -8.3, -7.0, -6.25, -5., -4.2, -2.4, -0.6,
    0.4, 1.4, 3.2, 5.05, 6.0, 6.9, 7.9, 8.75, 9.2, 10.25, 12.5])
  diag = np.array([1,1,1,1,1,1,1,2,1,2,2,2,2,2,2,2,2,2,2])
  unqDiags = np.unique(diag)
  nrDiags = unqDiags.shape[0]
  ysPoints = fSig(xsPoints)
  ysPointsPerturb = [0,0]
  print('xsPoints', xsPoints, ysPoints)
  diagLabels = ['Controls', 'Patients']

  ax = pl.gca()
  xLim = (xMin, xMax-9)
  yLim = (-4,8)
  xOrigin = 0
  from sklearn.neighbors.kde import KernelDensity
  kdes = []
  kdeXs = np.linspace(xLim[0], xLim[1], num=100).reshape(-1, 1)
  kernelWidth = np.std(xsPoints)/5.5 # need to test this parameter by visualisation
  for d in [1,2]:
    ysPointsPerturb[d-1] = ysPoints[diag == d] + np.random.normal(
      loc = 0, scale = 0.5, size = diag[diag == d].shape[0])
    ax.scatter(xsPoints[diag == d], ysPointsPerturb[d-1], marker = 'x',
      s = markerSize, linewidths = lw, c=diagCols[d], label = diagLabels[d-1])

    kdeCurr = KernelDensity(kernel='gaussian', bandwidth=kernelWidth).fit(
      xsPoints[diag == d].reshape(-1, 1))
    scores = np.exp(kdeCurr.score_samples(kdeXs))
    scaledScores = scores - np.min(scores) / (np.max(scores) - np.min(scores))
    scaledScores = scaledScores * (yLim[1] - yLim[0]) * 2 + yLim[0]

    pl.fill_between(kdeXs.reshape(-1), yLim[0], scaledScores,
      facecolor=diagCols[d], alpha=0.4)

    maxScore = np.max(scaledScores) + 0.25
    maxInd = np.argmax(scaledScores)
    pl.text(kdeXs[maxInd] - 1.5, maxScore, diagLabels[d-1], color=diagCols[d])


  pl.plot([xOrigin,xOrigin], [yLim[0], yLim[1]], '--', c=(0.5,0.5,0.5), linewidth=lw
    ,label='Disease onset'
  )

  # plt.plot(range(5), range(5), 'ro', markersize = 20, clip_on = False, zorder = 100)

  pl.xlim(xLim)
  pl.ylim(yLim)
  # pl.legend(ncol=2, loc='upper center')
  pl.legend(ncol=2, bbox_to_anchor=(0.05, 1.27, 0.95, .102))
  pl.xlabel('Years since $t_0$')
  pl.ylabel('Biomarker Z-Score')
  ax.set_yticks([-4,-2,0,2,4,6,8])
  ax.set_yticklabels(['', '', '-3', '-2', '-1', '0', '1'])
  # ax.set_xticks(ax.get_xticks()[1:-2] + xOrigin)
  # ax.set_xticklabels(['-10', '0', '10'])
  pl.gcf().subplots_adjust(left = 0.13,bottom=0.15,top=0.75)
  # ax.yaxis.set_label_coords(-0.1, 0.5)
  # ax.set_xlim((xLim[0] + xLimShift, xLim[1] + xLimShift))

  # boxprops = dict(linestyle = '--', linewidth = 3, color = 'blue')
  # medianprops = dict(linestyle = '-.', linewidth = 0.1, color = 'firebrick')
  # ax2 = pl.axes([0.03, 0, 0.1, 1], facecolor = (1, 1, 1, 0))
  # ax2.set_frame_on(False)
  # ax2.set_xlim((0,1))
  # ax2.set_ylim(yLim)
  # ax2.set_yticks([])
  # boxPos = [np.array([1.25]), np.array([1])]
  # # yDisp = [-0.3, 0.6]
  # yDisp = [-1.75, 0]
  # yScale = [1.2, 1]
  # yDisp = [11.5, 0]
  # yScale = [-1.2, 1]
  # nrDiags = 2
  # for d in range(nrDiags):
  #   print('ys %d ' % d, ysPointsPerturb[d]*yScale[d]+yDisp[d])
  #   bp = ax2.boxplot(ysPointsPerturb[d]*yScale[d]+yDisp[d], notch=0, sym='rs', vert=True, whis=1.75, widths=[0.1],
  #            positions=boxPos[d], showfliers=False, patch_artist=True, showmeans=True, medianprops=medianprops)
  #   pylab.setp(bp['boxes'], color = diagCols[unqDiags[d]])

  # make new axis ax3, with 0 - 1 limits
  # ax3 = pl.axes([0,0,1,1], facecolor=(1,1,1,0))
  # ax3.set_frame_on(False)
  #
  # #x,y = np.array([[0.05, 0.1, 0.9], [0.05, 0.5, 0.9]])
  # #line = lines.Line2D(x, y, lw=5., color='r', alpha=0.4)
  # ax3.set_xlim((0, 1))
  # ax3.set_ylim((0, 1))
  # # ax3.plot([0.1,0.56], [0.36, 0.36], '--', c=(0.5,0.5,0.5), linewidth=lw)
  # ax3.set_yticks([])
  # adjustFig(maxSize = (400, 400))
  fig.show()

  return fig

def integrateTrajOne(xs,dXdT_pred):
  # convert input vectors xs and dXdT into column vectors (nrPoints,1)

  # assert all(dXdT_pred < 0)

  dXdT_pred = np.matrix(dXdT_pred)
  xs = np.matrix(xs)
  if xs.shape[0] == 1:
    xs = xs.T
  if dXdT_pred.shape[0] == 1:
    dXdT_pred = dXdT_pred.T

  indices = np.array(range(len(xs)))
  dXs = (xs[indices] - xs[indices - 1])
  dXdivdXdT = np.divide(dXs, dXdT_pred[indices])
  t = np.cumsum(dXdivdXdT).T
  # print("integrateTraj", xs.shape, dXs.shape, dXdT_pred.shape, dXdivdXdT.shape, t.shape)
  #print t

  return t

def plotSingularity(figParams):

  (xsPoints, ysPoints, xsModel, ysModel, ysUpper, ysLower, xLim) = figParams

  tModel = integrateTrajOne(xsModel, ysModel)
  print('ysModel', ysModel)
  tModelPos = integrateTrajOne(xsModel[ysModel<0], ysModel[ysModel<0])
  xMin = np.min(tModelPos)
  xMax = np.max(tModelPos)
  # print()

  fig = pl.figure(1)
  pl.clf()

  pl.plot(tModel, xsModel)
  # pl.xlim([xMin, xMax])
  pl.xlim([-4.5,2])
  pl.xticks([])
  pl.yticks([])
  pl.xlabel('Time (years)')
  pl.ylabel('Biomarker value')

  fig.show()



  return fig



paramsFile = 'fig2_params.npz'



# fig1 = plotLinearRegr()
# fig1.savefig('fig1_linReg.png', dpi=100)

# fig2, figParams = plotGPfit()
# fig2.savefig('fig2_GP.png', dpi=100)
# dataStruct = dict(figParams=figParams)
# pickle.dump(dataStruct, open(paramsFile,'wb'), protocol=pickle.HIGHEST_PROTOCOL)

dataStruct = pickle.load(open(paramsFile, 'rb'))
# fig3 = plotTrajReconstruction(dataStruct['figParams'])
# fig3.savefig('fig3_recon.png', dpi=100)

fig4 = plotTrajAlignment()
fig4.savefig('fig4_align.png', dpi=100)

figParams = dataStruct['figParams']
# fig5 = plotSingularity(figParams)
# fig5.savefig('fig5_singularity.png', dpi=100)
