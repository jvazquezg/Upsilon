# only select between lin or log
import os, sys, time
from Useful_files import *


class Ini_file:
    def __init__(self, data_type, bin_type, redz):
        self.data_type = data_type
        self.bin_type  = bin_type
        self.redz      = redz
        self.fname     = files_name(data_type, bin_type, redz)

        self.R0        = R0_files()
        self.npoints   = number_of_points(data_type, bin_type)
        if len(self.R0) != len(self.npoints):  sys.exit("Error: check number of files")
        self.R0_points  = zip(self.R0, self.npoints)

        self.dir_chains = chain_dir(data_type)
        self.dir_data   = 'lrgdata-final/mocks_lrg/sim_reshaped/'
        self.dir_stats  = 'stats/'
        self.dir_bf     = 'bestfit/'

        self.name_root  = '_ups'
        self.name_ups   = '_ups.dat'
        self.name_cov   = '_cov.dat'
        self.name_dist  = 'distparams'

        self.aver       =  1.0




    def write_ini(self, R0, nR0, jk=None):
        if jk is not None: full_name = '%s%i%s'%(self.fname, R0, jk)
        else:              full_name = '%s%i'%(  self.fname, R0)
        print full_name

        with open('INI_%s.ini'%(full_name), 'w') as f:
            f.write(Text_ini_file())
            f.write(params_upsilon())
            f.write('use_upsilon= 98\n')
            f.write('samples  = 10000000\n')

            f.write('best_fit = %sbest_%s.dat\n'%(self.dir_bf, full_name))
            f.write('aver     = %1.2f\n'%(self.aver if 'rebin' in bin_type else 0))
            f.write(params_cosmo(self.data_type) + '\n\n')

            f.write('z_gg     = %s   \n'%(z_mean(self.data_type, self.redz)))
            f.write('z_gm     = %s   \n'%(z_mean(self.data_type, self.redz)))

            f.write(R0_params(R0, nR0) + '\n')
            f.write('use_diag = %s\n\n'%('F' if 'rebin' in self.bin_type else 'T'))

            f.write('file_root = ' + self.dir_chains + full_name + self.name_root + '\n')
            f.write('mock_file = ' + self.dir_data   + full_name + self.name_ups  + '\n')
            f.write('mock_cov  = ' + self.dir_data   + full_name + self.name_cov  + '\n')





    def write_bf(self, R0, run_bf=False):
        import pandas as pd
        full_name = '%s%i'%(self.fname, R0)

        file_bf = self.dir_stats + full_name + self.name_root + '.margestats'
        #names   = ['param','bestfit','lower1',
        #           'upper1','lower2','upper2','name','other']
	names   = ['param', 'mean', 'sddev', 'lowe1', 'upper1','limit1',
		 'lower2','upper2','limit2','name','other'] 	

        lines   =  pd.read_csv(file_bf, names= names, sep='\s+', skiprows=[0,1,2], index_col='param')
        print lines
	b1_bf   =  lines.ix['LRGa']['mean']
        b2_bf   =  lines.ix['LRGb']['mean']
        lna_bf  =  lines.ix['logA']['mean']

        with open('bf_INI_%s.ini'%(full_name), 'w') as f:
            f.write('param[LRGa] = %2.3f %2.3f %2.3f 0.001 0.001\n'%(b1_bf, b1_bf-0.001, b1_bf+0.001))
            f.write('param[LRGb] = %1.3f %1.3f %1.3f 0.001 0.001\n'%(b2_bf, b2_bf-0.001, b2_bf+0.001))
            f.write('param[logA] = %1.3f %1.3f %1.3f 0.001 0.001\n'%(lna_bf,lna_bf-0.001,lna_bf+0.001))
            f.write('use_upsilon = 99\n')
            f.write('samples     = 8\n')

            f.write(Text_ini_file())
            f.write('best_fit = %sbest_%s.dat\n'%(self.dir_bf, full_name))
            f.write('aver     = %1.2f\n'%(self.aver if 'rebin' in bin_type else 0))
            f.write(params_cosmo(self.data_type) + '\n\n')

            f.write('z_gg     = %s   \n'%(z_mean(self.data_type, self.redz)))
            f.write('z_gm     = %s   \n'%(z_mean(self.data_type, self.redz)))

            f.write(R0_params(R0, nR0) + '\n')
            f.write('use_diag = %s\n\n'%('F' if 'rebin' in self.bin_type else 'T'))

            f.write('file_root = ' + self.dir_chains + full_name + self.name_root + '\n')
            f.write('mock_file = ' + self.dir_data   + full_name + self.name_ups  + '\n')
            f.write('mock_cov  = ' + self.dir_data   + full_name + self.name_cov  + '\n')

        if run_bf:
            commd = './cosmomc bf_INI_%s.ini'%(full_name)
            os.system(commd)
            time.sleep(3.)


    def plot_bf(self, R0):
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

        full_name = '%sbest_%s%i.dat'%(self.dir_bf, self.fname, R0)
	
        names = ['r', 'obs', 'sig', 'theo']
        lines = pd.read_table(full_name, names=names, sep='\s+')
	split_lines = []
  	for nm in names:
           split_lines.append(np.array_split(lines[nm], 2))

        fig = plt.figure(figsize=(15,6))
        ax = fig.add_subplot(1,2,1)
        ax.errorbar(split_lines[0][0], split_lines[1][0], yerr=split_lines[2][0], fmt='+')
        ax.plot(split_lines[0][0], split_lines[3][0])
        plt.xlabel('r')
        plt.ylabel('gg')
        ax.set_title('%s, R0=%i'%(self.redz, R0))
        plt.legend(loc="upper right")

	
        ax2 = fig.add_subplot(1,2,2)
        ax2.errorbar(split_lines[0][1], split_lines[1][1], yerr=list(split_lines[2][1]), fmt='+')
        ax2.plot(split_lines[0][1], split_lines[3][1])
        plt.xlabel('r')
        plt.ylabel('gm')
        ax2.set_title('%s, R0=%i'%(self.redz, R0))
        plt.legend(loc="upper right")

        plt.tight_layout()
        plt.savefig(full_name.replace('.dat','') + ".pdf")
        plt.show()





    def write_dist(self, R0, jk=None, run_dist=False):
        txt='file_root=chains/Sim_rmin_gt_R0/Rmin_70_sim_z0.25_norsd_np0.001_nRT10_r02_ups'
        full_name = '%s%i'%(self.fname, R0)
        print full_name

        txt_new = 'file_root=' + self.dir_chains + full_name + self.name_root
        f1 = open(self.name_dist + '.ini', 'r')
        f2 = open(self.name_dist + '_%s.ini'%(full_name), 'w')

        for line in f1:
            f2.write(line.replace(txt, txt_new))
        f1.close()
        f2.close()

        if run_dist:
            commd = """./getdist %s_%s.ini"""%(self.name_dist, full_name)
            os.system(commd)
            time.sleep(0.5)




    def write_wq(self, R0, jk=None, run_wq=False, nodes=12, threads=3):
        if jk is not None: full_name = '%s%i%s'%(self.fname, R0, jk)
        else:              full_name = '%s%i'%(  self.fname, R0)
        print full_name

        with open('wq_%s.ini'%(full_name), 'w') as f:
            f.write('mode: bycore\n')
            f.write('N: %i\n'%(nodes))
            f.write('threads: %i\n'%(threads))
            f.write('hostfile: auto\n')
            f.write('job_name: %s\n'%(full_name))
            f.write('command: |\n')
            f.write('    source ~/.bashrc; \n')
            f.write('    OMP_NUM_THREADS=%%threads%% mpirun -hostfile %%hostfile%% '
                    './cosmomc INI_%s.ini > %slogs/INI_%s.log 2>%slogs/INI_%s.err'%(full_name, self.dir_chains,full_name,self.dir_chains,full_name))

        if run_wq:
            commd="""nohup wq sub wq_%s.ini &"""%(full_name)
            os.system(commd)
            time.sleep(1.)






if __name__=='__main__':

    mocks = False
    if mocks:
       data_type = 'mocks'
       bin_type ='rebin1'
       redzz = ['singlesnap','allsnap', 'evol']
    else:
       data_type = 'lowz'
       bin_type = 'log1_rebin'
       redzz = ['lowz']

    for redz in redzz:
    	Ini = Ini_file(data_type, bin_type, redz)
    	for R0_points in Ini.R0_points:
	    R0, nR0 = R0_points  
            if True:
		print R0_points 
        	#Ini.write_ini(R0, nR0)
        	#Ini.write_wq(R0, run_wq=True, nodes=15)
		Ini.write_dist(R0, run_dist=True)
        	Ini.write_bf(R0, run_bf=True)
        	Ini.plot_bf(R0)