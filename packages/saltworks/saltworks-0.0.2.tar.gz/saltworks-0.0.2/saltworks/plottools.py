import matplotlib
import matplotlib.collections as mcoll
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

from .indextools import make_index
from .robuststat import mad, robust_average


color_cycle = [(166, 206, 227), (31, 120, 180), (178, 223, 138), (51, 160, 44)]
color_cycle = [(r / 256., g / 256., b / 256.) for r, g, b in color_cycle]


def binplot(x, y, nbins=10, robust=False, data=True,
            scale=True, bins=None, weights=None, ls='none',
            dotkeys={'color': 'k'}, xerr=True, ax=None, **keys):
    """ Bin the y data into n bins of x and plot the average and
    dispersion of each bins.

    Arguments:
    ----------
    nbins: int
      Number of bins

    robust: bool
      If True, use median and nmad as estimators of the bin average
      and bin dispersion.

    data: bool
      If True, add data points on the plot

    scale: bool
      Whether the error bars should present the error on the mean or
      the dispersion in the bin

    bins: list
      The bin definition

    weights: array(len(x))
      If not None, use weights in the computation of the mean.
      Provide 1/sigma**2 for optimal weighting with Gaussian noise

    dotkeys: dict
      To keys to pass to plot when drawing data points

    ax: matplotlib axes instance. If None plot to the current axes

    **keys:
      The keys to pass to plot when drawing bins

    Exemples:
    ---------
    >>> x = np.arange(1000); y = np.random.rand(1000);
    >>> binplot(x,y)
    """
    ind = ~np.isnan(x) & ~np.isnan(y)
    x = x[ind]
    y = y[ind]
    if weights is not None:
        weights = weights[ind]
    if bins is None:
        bins = np.linspace(x.min(), x.max() + abs(x.max() * 1e-7), nbins + 1)
    ind = (x < bins.max()) & (x >= bins.min())
    x = x[ind]
    y = y[ind]
    if weights is not None:
        weights = weights[ind]
    yd = np.digitize(x, bins)
    index = make_index(yd)
    ybinned = [y[e] for e in index]
    xbinned = 0.5 * (bins[:-1] + bins[1:])
    usedbins = np.array(np.sort(list(set(yd)))) - 1
    xbinned = xbinned[usedbins]
    bins = bins[usedbins + 1]
    if ax is None and not 'noplot' in keys:
        ax = plt.gca()
    if data and not 'noplot' in keys:
        ax.plot(x, y, ',', **dotkeys)

    if robust is True:
        yplot = [np.median(e) for e in ybinned]
        yerr = np.array([mad(e) for e in ybinned])
    elif robust:
        yres = [robust_average(e, sigma=None, clip=robust, mad=False, axis=0)
                for e in ybinned]
        yplot = [e[0] for e in yres]
        yerr = [np.sqrt(e[3]) for e in yres]
    elif weights is not None:
        wbinned = [weights[e] for e in index]
        yplot = [np.average(e, weights=w) for e, w in zip(ybinned, wbinned)]
        if not scale:
            #yerr = np.array([np.std((e - a) * np.sqrt(w))
            #                 for e, w, a in zip(ybinned, wbinned, yplot)])
            yerr = np.array([np.sqrt(np.std((e - a) * np.sqrt(w)) ** 2 / sum(w))
                             for e, w, a in zip(ybinned, wbinned, yplot)])
        else:
            yerr = np.array([np.sqrt(1 / sum(w))
                             for e, w, a in zip(ybinned, wbinned, yplot)])
        scale = False
        print(yplot)
    else:
        yplot = [np.mean(e) for e in ybinned]
        yerr = np.array([np.std(e) for e in ybinned])

    if scale:
        yerr /= np.sqrt(np.bincount(yd)[usedbins + 1])

    if xerr:
        xerr = np.array([bins, bins]) - np.array([xbinned, xbinned])
    else:
        xerr = None
    if not 'noplot' in keys:
        ax.errorbar(xbinned, yplot, yerr=yerr,
                     xerr=xerr,
                     ls=ls, **keys)
    return xbinned, yplot, yerr


def bplot(x, y, data=True, binkey=None, robust=False, scale=True, ls='none', marker='s', **keys):
    if x.shape != y.shape: raise ValueError('x and y have different length')
    if binkey is None:
        binkey = x
    ind = make_index(binkey)
    ybinned = [y[e] for e in ind]
    xbin = [x[e] for e in ind]
    if data:
        plt.plot(x, y, ',', color='k')

    if robust is True:
        yplot = [np.median(e) for e in ybinned]
        yerr = np.array([mad(e) for e in ybinned])
    elif robust:
        yres = [robust_average(e, sigma=None, clip=robust, mad=False, axis=0)
                for e in ybinned]
        yplot = [e[0] for e in yres]
        yerr = [np.sqrt(e[3]) for e in yres]
    else:
        yplot = [np.mean(e) for e in ybinned]
        yerr = np.array([np.std(e) for e in ybinned])

    if scale:
        yerr /= np.sqrt(np.array([len(e) for e in ybinned]))
    xplot = [np.mean(e) for e in xbin]
    plt.errorbar(xplot, yplot, yerr=yerr, ls=ls, marker=marker, **keys)
    return xplot, yplot, yerr


def plotpolyfit(x, y, yerr=None, deg=1, stat_legend=False, return_result=False, **keys):
    """
    Uses polyfit and plots the result

    If stat_legend is set, prints the plot results in legend.
    If return_result is set, returns the polyfit p and the linspace lx
    """
    ls = keys.pop('ls', 'none')
    marker = keys.pop('marker', 's')
    plt.errorbar(x, y, yerr=yerr, ls=ls, marker=marker, **keys)
    if yerr is not None:
        w = 1 / yerr ** 2
    else:
        w = None
    p, cov = np.polyfit(x, y, w=w,  deg=deg, cov=True)
    r = y - np.polyval(p, x)

    axrange = plt.axis()[:2]
    lx = np.linspace(*axrange)
    if stat_legend:
        plt.plot(
            lx,
            np.polyval(p, lx),
            'k-',
            label="%3.2f ($\pm$ %2.1e) x + %3.2f ($\pm$ %2.1e)\n rms: %5.3f" % (
                p[0],
                cov[0][0],
                p[1],
                cov[1][1],
                np.std(r)))
        plt.legend(prop={"size" : 9})
    else:
        plt.plot(lx, np.polyval(p, lx), 'k-')

    if return_result:
        return p, lx


def histofit(x, **keys):
    """Fits a 1D histogram to x

    heart=[start, end] keyword defines the heart of the distribution that will
    be fit

    """
    i_ok = np.isfinite(x)
    if np.any(~ i_ok):
        print(("Found %d not-finite values in x" % (len(np.where(~ i_ok)[0]))))
    x = x[i_ok]

    plt.rc('legend', fancybox=True)
    heart = keys.pop('heart', False)
    h, b, p = plt.hist(x, density=True, **keys)
    import scipy.stats
    if heart:
        m, sig = scipy.stats.distributions.norm.fit(
            x[(x > heart[0]) & (x < heart[1])])
        n = len(x[(x > heart[0]) & (x < heart[1])])
    else:
        m, sig = scipy.stats.distributions.norm.fit(x)
        n = len(x)
    plt.plot(b, scipy.stats.distributions.norm.pdf(b, m, sig),
             label='mean: %.3g\nsig: %.3g' % (m, sig))
    plt.gca().legend(loc=1, ncol=1, shadow=True)
    return m, sig, sig / np.sqrt(n)


def histofit2(x, **keys):
    # TODO why changing default ???
    plt.rc('legend', fancybox=True)
    range = keys.pop('range', [x.min(), x.max()])
    h, b, p = plt.hist(x, range=range, density=True, **keys)
    index = h > 0
    #p, e = np.polyfit(0.5 * (b[1:] + b[:-1])[index],
    #                  np.log(h[index]),
    #                  h[index] ** 2, 2)
    from .robuststat import polyfit
    p, e = polyfit((b[1:])[index], np.log(h[index]), h[index], 2)
    a, b, c = p
    sigma = 1 / np.sqrt(-2 * a)
    x0 = b * sigma ** 2
    A = np.exp(c + x0 ** 2 / (2 * sigma ** 2))
    l = np.linspace(*range)
    plt.plot(l, A * np.exp(-(l - x0) ** 2 / (2. * sigma ** 2)),
             label='mean: %.3g\nsig: %.3g' % (x0, sigma))
    plt.gca().legend(loc=1, ncol=1, shadow=True)
    return x0, sigma


def aa_plot(twocols=False, height=None):
    """Change settings to obtain plots nicely suited for A&A publications"""
    linewidth = 3.53972  # inches
    textwidth = 7.2455   # inches
    width = textwidth if twocols else linewidth
    if not height:
        height = 2.7
    plt.rc('figure', figsize=(width, height))
    #plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'], 'size': 10})
    plt.rc('font', **{'family':'serif'})
    plt.rc('axes', labelsize='small')
    #plt.rc('grid', alpha='0.5')
    plt.rc('grid', linewidth='0.1')
    plt.rc('grid', linestyle='-')
    plt.rc('grid', color='0.3')
    plt.rc('lines', markersize=3)
    plt.rc('xtick', labelsize='x-small')
    plt.rc('xtick.major', pad=2)
    plt.rc('ytick', labelsize='x-small')
    plt.rc('ytick.major', pad=2)
    plt.rc('axes', linewidth=0.1)
    plt.rc('text', usetex=True)
    #plt.rc('axes', edgecolor='0.5')
    plt.rc('text.latex', preamble=r'\usepackage{txfonts}')
    #plt.rc('ps', usedistiller='xpdf')
    plt.rc('xtick.major', size=3)
    plt.rc('xtick.minor', size=1)
    plt.rc('ytick.major', size=3)
    plt.rc('ytick.minor', size=1)
    #plt.rc('ytick', color='0.5')
    #plt.rc('xtick', color='0.5')
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'

    plt.rc('legend', fontsize='x-small')
    #plt.rc('axes', color_cycle = color_cycle)


def density_plot(x, y, bins=(50, 50), nlev=5):
    """ Density contour
    """
    h, x_b, y_b = np.histogram2d(x, y, bins=bins)
    x_m = 0.5 * (x_b[:-1] + x_b[1:])
    y_m = 0.5 * (y_b[:-1] + y_b[1:])
    X, Y = np.meshgrid(x_m, y_m)
    xd = np.digitize(x, x_b) - 1
    # digitize exclude the right hand of the bin
    xd[xd == len(x_m)] = len(x_m) - 1
    yd = np.digitize(y, y_b) - 1
    yd[yd == len(y_m)] = len(y_m) - 1
    levels = np.exp(np.linspace(np.log(2), np.log(h.max()), nlev + 1))[:-1]
    C = plt.contour(X.T, Y.T, h, levels=levels)
    index = h[xd, yd] < C.levels[0]
    plt.plot(x[index], y[index], ',')


def inline_legend(axis=None, **keys):
    if axis is None:
        axis = plt.gca()
    ls = LineSet(axis)
    ls.clabel(**keys)
    plt.draw_if_interactive()


class LineSet(matplotlib.contour.ContourLabeler):
    def __init__(self, ax):
        self.axes = ax
        self.lines = [l for l in ax.lines]
        self.labelTexts = []
        self.labelCValues = []
        self.levels = [l.get_label() for l in ax.lines]
        self.cvalues = list(range(len(ax.lines)))  # [l.get_label() for l in ax.lines]
        self.collections = matplotlib.cbook.silent_list('mcoll.LineCollection')
        self.alpha = None
        self._contour_zorder = 0
        for l in self.lines:
            col = mcoll.LineCollection(
                [l.get_xydata()],
                antialiaseds=[l.get_antialiased()],
                linewidths=[l.get_linewidth()],
                linestyle=[l.get_linestyle()],
                colors=[l.get_color()],
                alpha=l.get_alpha(),
                transform=l.get_transform(),
                zorder=l.get_zorder())
            l.remove()
            self.axes.add_collection(col)
            self.collections.append(col)
        #.get_xydata()
        #self.levels = kwargs.get('levels', None)

    def to_rgba(self, cv, alpha=None):
        return matplotlib.colors.colorConverter.to_rgba(
            self.lines[cv].get_color())


snlsfield_color = {
    'D1': 'r',
    'D2': 'g',
    'D3': 'k',
    'D4': 'b'}


snlsfield_marker = {
    'D1': '+',
    'D2': 's',
    'D3': 'o',
    'D4': 'x'}


band_color = {
    'u': 'm',
    'g': 'g',
    'r': 'r',
    'i': 'k',
    'i2': 'c',
    'z': 'b'}


band_marker = {
    'u': '+',
    'g': 's',
    'r': 'o',
    'i': 'p',
    'i2': 'D',
    'z': 'x'}


def rstyle(ax):
    """Styles an axes to appear like ggplot2

    Must be called after all plot and axis manipulation operations have been
    carried out (needs to know final tick spacing)

    """
    #set the style of the major and minor grid lines, filled blocks
    ax.grid(True, 'major', color='w', linestyle='-', linewidth=1.4)
    ax.grid(True, 'minor', color='0.92', linestyle='-', linewidth=0.7)
    ax.patch.set_facecolor('0.85')
    ax.set_axisbelow(True)

    #set minor tick spacing to 1/2 of the major ticks
    ax.xaxis.set_minor_locator(plt.MultipleLocator((plt.xticks()[0][1]-plt.xticks()[0][0]) / 2.0 ))
    ax.yaxis.set_minor_locator(plt.MultipleLocator((plt.yticks()[0][1]-plt.yticks()[0][0]) / 2.0 ))

    #remove axis border
    for child in ax.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_alpha(0)

    #restyle the tick lines
    for line in ax.get_xticklines() + ax.get_yticklines():
        line.set_markersize(5)
        line.set_color("gray")
        line.set_markeredgewidth(1.4)

    #remove the minor tick lines
    for line in ax.xaxis.get_ticklines(minor=True) + ax.yaxis.get_ticklines(minor=True):
        line.set_markersize(0)

    #only show bottom left ticks, pointing out of axis
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    if ax.legend_ != None:
        lg = ax.legend_
        lg.get_frame().set_linewidth(0)
        lg.get_frame().set_alpha(0.5)


def rhist(ax, data, **keywords):
    """Creates a histogram with default style parameters to look like ggplot2

    Is equivalent to calling ax.hist and accepts the same keyword parameters.
    If style parameters are explicitly defined, they will not be overwritten

    """
    defaults = {
        'facecolor' : '0.3',
        'edgecolor' : '0.28',
        'linewidth' : '1',
        'bins' : 100}

    for k, v in list(defaults.items()):
        if k not in keywords: keywords[k] = v

    return ax.hist(data, **keywords)


def rbox(ax, data, **keywords):
    """Creates a ggplot2 style boxplot

    It is equivalent to calling ax.boxplot with the following additions:

    Keyword arguments:
    colors -- array-like collection of colours for box fills
    names -- array-like collection of box names which are passed on as tick labels

    """
    import pylab
    hasColors = 'colors' in keywords
    if hasColors:
        colors = keywords['colors']
        keywords.pop('colors')

    if 'names' in keywords:
        ax.tickNames = plt.setp(ax, xticklabels=keywords['names'] )
        keywords.pop('names')

    bp = ax.boxplot(data, **keywords)
    pylab.setp(bp['boxes'], color='black')
    pylab.setp(bp['whiskers'], color='black', linestyle = 'solid')
    pylab.setp(bp['fliers'], color='black', alpha = 0.9, marker= 'o', markersize = 3)
    pylab.setp(bp['medians'], color='black')

    numBoxes = len(data)
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
          boxX.append(box.get_xdata()[j])
          boxY.append(box.get_ydata()[j])
        boxCoords = list(zip(boxX,boxY))

        if hasColors:
            boxPolygon = Polygon(boxCoords, facecolor = colors[i % len(colors)])
        else:
            boxPolygon = Polygon(boxCoords, facecolor = '0.95')

        ax.add_patch(boxPolygon)

    return bp


def histequ_colormap(image_data, lower_bound=None, upper_bound=None):
    """Creates an histogram equalization colormap of the data

    use with cmap=histequ_colormap(image_data). Taken from
    http://stackoverflow.com/questions/5858902

    """
    data = image_data[np.isfinite(image_data)]
    image_sort = np.sort(data.flatten())
    if lower_bound is None:
        lower_bound = image_sort[0]
    if upper_bound is None:
        upper_bound = image_sort[-1]

    i_ok = (image_sort < upper_bound) & (image_sort > lower_bound)
    image_sort_ok = image_sort[i_ok]
    # See https://en.wikipedia.org/wiki/Histogram_equalization
    l_step = (image_sort_ok[::len(image_sort_ok)/256] - lower_bound) / (upper_bound - lower_bound)
    n_step = float(len(l_step))

    # For edge effects, the data mapping must start at 0 and go to 1
    l_step[0] = min(0., l_step[0])
    l_step[-1] = min(1., l_step[-1])

    interps = [(s, idx/n_step, idx/n_step) for idx, s in enumerate(l_step)]
    interps.append((1, 1, 1))
    cdict = {'red' : interps,
             'green' : interps,
             'blue' : interps}
    histequ_cmap = matplotlib.colors.LinearSegmentedColormap('HistEq', cdict)

    return histequ_cmap


def wavelength_to_rgb(wavelength, gamma=0.8):
    """Converts a given wavelength of light to an approximate RGB color value

    The wavelength must be given in nanometers in the range from 380 nm through
    750 nm (789 THz through 400 THz).

    Taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html

    Additionally alpha value set to 0.5 outside range

    """
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A=0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength >750:
        wavelength = 750.
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R,G,B,A)


# if __name__ == "__main__":
#     x = np.arange(1000)
#     y = np.random.randn(1000)
#     binplot(x, y)
#     plt.show()
