import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

def findNplot(file_address, column_name, img_name, img_addr,plot_title, marker, x_name, y_name, plot=False):
    d=pd.read_excel(file_address)
    ndf=d.filter(items=[column_name])

    if plot==True:
            yp1=np.array(ndf[column_name].tolist())
            plt.plot(yp1,marker)
            plt.title(plot_title)
            plt.xlabel(x_name)
            plt.ylabel(y_name)

            fig=plt.gcf()
            plt.show()
            plt.draw()
            img_addr=img_addr+img_name
            fig.savefig(img_addr+'.jpg', dpi=100)
    else:
        return ndf