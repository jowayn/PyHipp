import numpy as np 
import DataProcessingTools as DPT 
from .rpllfp import RPLLFP 
from .rplhighpass import RPLHighPass
from .rplraw import RPLRaw
from .helperfunctions import computeFFT
import matplotlib.pyplot as plt
import os 
from .misc import getChannelInArray

plt.rcParams['font.size'] = 6

class FreqSpectrum(DPT.DPObject):

	filename = "freqspectrum.hkl"
	argsList = [('loadHighPass', False), ('loadRaw', False), ('pointsPerWindow', 2000)]
	level = 'channel'

	def __init__(self, *args, **kwargs):
		DPT.DPObject.__init__(self, *args, **kwargs)

	def create(self, *args, **kwargs):
		pwd = os.path.normpath(os.getcwd());
		self.freq = []
		self.magnitude = []
		self.numSets = 0 
		if self.args['loadHighPass']:
			rpdata = RPLHighPass()
		elif self.args['loadRaw']:
			rpdata = RPLRaw()
		else: 
			rpdata = RPLLFP()
		dlength = len(rpdata.data)
		ppw = self.args['pointsPerWindow']
		if dlength > 0: 
			DPT.DPObject.create(self, *args, **kwargs)
			# pad rpdata to make sure we can reshape into desired length
			rpdata1 = np.pad(rpdata.data,(0,int(np.ceil(dlength/ppw)*ppw)-dlength))
			# reshape so data is in columns
			rpdata2 = np.reshape(rpdata1,(ppw,-1), order='F')
			# compute the mean of each column so we can demean the data
			rp2mean = rpdata2.mean(axis=0)
			# subtract the mean so the DC value will be 0
			rpdata3 = rpdata2 - rp2mean[np.newaxis, :]
			magnitude, freq = computeFFT(rpdata3, rpdata.analogInfo['SampleRate'])
			self.freq = [freq]
			# take the mean of the magnitude across windows
			self.magnitude = [magnitude.mean(axis=1)]
			# take the stderr of the magnitude across windows
			self.magstderr = [magnitude.std(axis=1) / np.sqrt(np.size(rpdata2,1))]
			self.numSets = 1
			# self.title = [DPT.levels.get_shortname("channel", pwd)[-3:]]
            # get array name
			aname = DPT.levels.normpath(os.path.dirname(pwd))
            # store array name so we can do the array plot more easily
			self.array_dict = dict()
			self.array_dict[aname] = 0
            # this is used to compute the right index when switching between plot types
			self.current_plot_type = None
		else: 
			DPT.DPObject.create(self, dirs=[], *args, **kwargs)   
		return 

	def append(self, fs):
		DPT.DPObject.append(self, fs)
		self.magnitude += fs.magnitude
		self.magstderr += fs.magstderr
		self.freq += fs.freq
		# self.title += fs.title
        # loop through array dictionary in fs
		for ar in fs.array_dict:
			self.array_dict[ar] = self.numSets
		self.numSets += 1

	def plot(self, i = None, ax = None, getNumEvents = False, getLevels = False, getPlotOpts = False, overlay = False, **kwargs):

		plotOpts = {'PlotType': DPT.objects.ExclusiveOptions(['Channel', 'Array'], 0), 'LabelsOff': False, 'TitleOff': False, 'TicksOff': False, 'XLims': []}

        # update the plotOpts based on kwargs, these two lines are important to
        # receive the input arguments and act accordingly
		for (k, v) in plotOpts.items():
			plotOpts[k] = kwargs.get(k, v)  

		if getPlotOpts:
			return plotOpts

		plot_type = plotOpts["PlotType"].selected()

		if self.current_plot_type is None:  # initial assignement of self.current_plot_type
			self.current_plot_type = plot_type

		if getNumEvents:
			if self.current_plot_type == plot_type:  # no changes to plot_type
				if plot_type == 'Channel':
					return self.numSets, i
				elif plot_type == 'Array':
					return len(self.array_dict), i
			elif self.current_plot_type == 'Array' and plot_type == 'Channel':  # change from array to channel
				if i == 0:
					return self.numSets, 0
				else:
					# get values in array_dict
					advals = np.array([*self.array_dict.values()])
					return self.numSets, advals[i-1]+1
			elif self.current_plot_type == 'Channel' and plot_type == 'Array':  # change from channel to array
				# get values in array_dict
				advals = np.array([*self.array_dict.values()])
				# find index that is larger than i
				vi = (advals >= i).nonzero()
				return len(self.array_dict), vi[0][0]

		if ax is None:
			ax = plt.gca()

		if not overlay:
			ax.clear()

		if plot_type == 'Channel':
			if self.current_plot_type == 'Array':
				fig = ax.figure  # get the parent figure of the ax
				for x in fig.get_axes():  # remove all axes in current figure
					x.remove()    
				ax = fig.add_subplot(1,1,1)
                
			# plot the mountainsort data according to the current index 'i'
			self.plot_data(i, ax, plotOpts, 1)
			self.current_plot_type = 'Channel'
    
		elif plot_type == 'Array':  # plot in channel level
			fig = ax.figure  # get the parent figure of the ax
			for x in fig.get_axes():  # remove all axes in current figure
				x.remove()    

			# get values in array_dict
			advals = np.array([*self.array_dict.values()])
			# get first channel, which will be the last index in the previous array plus 1
			if i == 0:
				cstart = 0
				cend = advals[0]
			else:
				cstart = advals[i-1] + 1
				cend = advals[i]
            
			currch = cstart
			plotOpts['LabelsOff'] = True
			plotOpts['TitleOff'] = True
			# plotOpts['TicksOff'] = True
			while currch <= cend :
				# get channel name
				currchname = self.dirs[currch]
				# get axis position for channel
				ax,isCorner = getChannelInArray(currchname, fig)
				self.plot_data(currch, ax, plotOpts, isCorner)
				currch += 1

			self.current_plot_type = 'Array'

	def plot_data(self, i, ax, plotOpts, isCorner):
		y = self.magnitude[i]
		x = self.freq[i]
		e = self.magstderr[i]
		ax.plot(x, y)
		# show the stderr by adding a shaded area around the y values
		ax.fill_between(x, y-e, y+e, alpha=0.5)
		ax.ticklabel_format(axis='both', style='sci', scilimits=(0,3))
		
		if (not plotOpts['TitleOff']) or isCorner:
			ax.set_title(self.dirs[i])

		if (not plotOpts['LabelsOff']) or isCorner:
			ax.set_xlabel('Freq (Hz)')
			ax.set_ylabel('Magnitude')

		if plotOpts['TicksOff'] or (not isCorner):
			ax.set_xticklabels([])
			ax.set_yticklabels([])

		if len(plotOpts['XLims']) > 0: 
			ax.set_xlim(plotOpts['XLims'])
		else: 
			if self.args['loadHighPass']:
				ax.set_xlim([500, 7500])
			elif self.args['loadRaw']:
				ax.set_xlim([0, 10000])
			else:
				ax.set_xlim([0, 150])
