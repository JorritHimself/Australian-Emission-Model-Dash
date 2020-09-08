# Australian emissions model in Python/Plotly/Dash


## How to import in local installation
Easiest is to use anaconda navigator.  
Go to 'environments', impot, and select the environment.yml file. 

Alternatively, via conda:  
`conda env create -f environment.yml`
followed by  
`activate ausenergydash`

## How to make it work in python anywhere
Copy the contents of WSIG for python anywhere.txt into the pyhton anywhere, in the web tab  
Make sure you change the run the app with:  
 `if __name__ == '__main__':
`
 `app.run_server()`  
Import the prepped data
 correctly with full directory:  
`df_final = pd.read_csv('/home/JorritHimself/mysite/db/preppeddata.csv')`



