for f in range(10):
  if f == 5:
    print '\n'
  if f == 0 or f ==5:
    #print r''
    print r'\begin{subfigure}[b]{0.223\textwidth}'
    print r'\centering'
    print 'f=%d' % (f+1)
    print r'\includegraphics[width=\linewidth, trim=22 0 35 20,clip]{\adniThickCVFolder/'+ 'f%d/trajSamplesOneFig_cogCorr_\\adniThickCVExpName_f%d.png}' % (f, f)

  else:
    print r'\begin{subfigure}[b]{0.185\textwidth}'
    print r'\centering'
    print 'f=%d' % (f+1)
    print r'\includegraphics[width=\linewidth, trim=75 0 35 20,clip]{\adniThickCVFolder/'+ 'f%d/trajSamplesOneFig_cogCorr_\\adniThickCVExpName_f%d.png}' % (f, f)

  print r'\end{subfigure}%    <-- % added here'
  print r'\hfill'

