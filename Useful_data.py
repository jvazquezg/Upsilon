

class Useful_data:
    def __init__(self, name='Upsilon'):
        self.name = name

    def file_choice(self, data_type):
        #"""Select the type of file to analyze"""

        if 'sim' in data_type:
            bin_type = 'lin_rebin1'          # lin or log / bin or rebin
            redz = ['0.25']                  # ['0.25','0.40']
            dir  = 'sim_results/'

        elif 'mocks' in data_type:
            bin_type = 'rebin1'              # lin1 or rebin1
            redz = ['singlesnap']            # ['singlesnap', 'allsnap', 'evol']
            dir  = 'mock_results/'

        elif 'lowz' in data_type:
            bin_type = 'log1_rebin'          # log1 or log1_rebin
            redz = ['lowz']                  # ['lowz', 'z1', 'z2']
            dir = 'lowz_results/'

        return bin_type, redz, dir



    def files_name(self, data_type, bin_type, redz):
                #Select name of the file
            if 'sim' in data_type:
                file_name = data_type +'_'+ bin_type +'_z'+ redz +'_norsd_np0.001_nRT10_r0'
            elif 'mocks' in data_type:
                file_name = 'mock_bigMD_RST_' + redz + '_' + bin_type + '_DM1_r0'
            elif 'lowz' in data_type:
                file_name =  redz + '_' + bin_type + '_r0'
            else:
                print 'error'

            return file_name


    def R0_files(self):
        lnum = 2, 3, 4, 5, 6, 10
        return lnum


if __name__ == '__main__':
    Ud = Useful_data()
    print Ud.file_choice('sim')