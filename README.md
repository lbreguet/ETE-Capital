# Senior Project

## A stock market graph generator

### I. Purpose
The purpose of this project is to find and analyze financial data where it is available. Nowadays you have to pay a lot of money to retrieve stock market data, just like on a `Bloomberg Terminal`. This project was an exercise to maybe one day create my own `Terminal`. Here we are looking at a political financial market. 
The API comes from `Predictit`, a web platform created by Victoria University of Wellington, New Zealand. 

### II. Dependencies
Run the command `sh install.sh` in your terminal to get all the dependencies needed to run this program.

### III. Code
Most of this project is written in `python`, but there are a few scripts for running the program and installing dependencies. The modules used are `json`, `openpyxl`, `os`, `pandas`, and `requests` from `urllib`.

 We'll now go through each function definition.
```py
def read_xml(url):

    r = requests.get(url)

    return r.content
```
What this method does is get the `response` from the `url` given and return the `content` of the response. However, the `content` is given back in `bytes` so we need a method to decode it.


```py
def bytes_to_str(data):

    return data.decode()
```
As the name of the method suggests, it takes the data and decodes the `bytes` to a `string` variable.
```py
def get_markets():
    
    data = bytes_to_dict(read_xml('https://www.predictit.org/api/marketdata/all'))
   
    data = json.loads(data)
    markets = data['markets']  
    
    return markets
```
Here we can see that we are pulling data in from a `url`. We also see that before the data is instantiated, it goes through the two methods seen before. We then load the data into a `json` object so that it can be treated as a `dict`. Lastly it returns the data we want to use which are the markets.

The next step to do is convert this data to an excel file.
```py
def to_xl():
    if (not path.exists("markets")):
        mkdir("markets")

    markets = get_markets()

    for market in markets:
        market['shortName'] = market['shortName'].replace("?", "_").replace("/", "-").replace("'", "").replace("\"", "")
        filepath = 'markets/' + market['shortName'] + '.xlsx'
        if (path.exists(filepath)):
            
            xl = pd.read_excel(filepath)
        
            contracts = market['contracts']
            df = pd.DataFrame(contracts)
            df['timeStamp'] = market['timeStamp']
            del df['id']
            del df['name']
            del df['status']
            del df['dateEnd']
            del df['image']
            del df['displayOrder']
            
            df_xl = xl
            
            df_new = pd.concat([df, df_xl])
            df_new = df_new.sort_values(by=['shortName', 'timeStamp'])
            try:
                remove(filepath)
            writer = pd.ExcelWriter(filepath, engine='openpyxl')
            df_new.to_excel(writer, index=False)
            
            
            writer.save()
            writer.close()

        else:
            
            writer = pd.ExcelWriter(filepath, engine='openpyxl')

            contracts = market['contracts']
            df = pd.DataFrame(contracts)
            df['timeStamp'] = market['timeStamp']
            del df['id']
            del df['name']
            del df['status']
            del df['dateEnd']
            del df['image']
            del df['displayOrder']
            df.to_excel(writer, index=False)
           
            writer.save()
            writer.close()
```
This method allows to generate excel files in a generated folder, if the folder doesn't exist already.
We then retrieve the market data from the previous method and loop through like so:
```py
if (not path.exists("markets")):
    mkdir("markets")

markets = get_markets()

for market in markets:
```

Now we have to manipulate the name of the market data because we will be using that name for our files. 
We also define a filepath used to save them in a specific location.
```py
market['shortName'] = market['shortName'].replace("?", "_").replace("/", "-").replace("'", "").replace("\"", "")
filepath = 'markets/' + market['shortName'] + '.xlsx'
```

The next step is to check if the specified file exists or not. For clarity's sake, the file doesn't exist yet: 
```py
else:
            
    writer = pd.ExcelWriter(filepath, engine='openpyxl')

    contracts = market['contracts']
    df = pd.DataFrame(contracts)
    df['timeStamp'] = market['timeStamp']
    del df['id']
    del df['name']
    del df['status']
    del df['dateEnd']
    del df['image']
    del df['displayOrder']
    df.to_excel(writer, index=False)
           
    writer.save()
    writer.close()
```
Using the `pandas` module we create an excel file with the specified `filepath` and we also put the list of contracts into a variable. This list is then made into a `DataFrame` and then we'll add and remove columns to the dataframe at our convenience.
The `DataFrame` is then pushed to the `ExcelWriter` object. We save the file and then close it.

If the file does exist we do the following:
```py
if (path.exists(filepath)):
            
    xl = pd.read_excel(filepath)
        
    contracts = market['contracts']
    df = pd.DataFrame(contracts)
    df['timeStamp'] = market['timeStamp']
    del df['id']
    del df['name']
    del df['status']
    del df['dateEnd']
    del df['image']
    del df['displayOrder']
            
    df_new = pd.concat([df, xl])
    df_new = df_new.sort_values(by=['shortName', 'timeStamp'])
    try:
        remove(filepath)
    writer = pd.ExcelWriter(filepath, engine='openpyxl')
    df_new.to_excel(writer, index=False)
            
            
    writer.save()
    writer.close()
```
We use the `pandas` module to read from the excel file and we also put the list of contracts into a variable. This list is then made into a `DataFrame` and then we'll add and remove columns to the dataframe at our convenience.
Now we must concat our current contracts with the ones in the excel file. We get our new `DataFrame`.
To make things easier when we're creating graphs, we will sort the data here and also try to delete the file so that we don't have many of the same graphs in the same sheet.
So we create the file again with the desired filepath and push the new `DataFrame` to it. Just like before, we save and close the `ExcelWriter` object.

Once we have all of our excel files ready we can start generating the line charts.
```py
def create_charts():
    to_xl()
    excels = listdir('markets')
    
    for excel in excels:
        filepath = 'markets/' + excel
        writer = pd.ExcelWriter(filepath , engine='openpyxl')
        df = pd.read_excel(filepath)
        workbook = load_workbook(filepath)
        writer.book = workbook
        
        worksheet=writer.book.worksheets[0]
        total_elems = 0
        
        dups_name = df.pivot_table(index=['shortName'], aggfunc='size')
        unique_names = df.shortName.unique()
        
        if (len(dups_name) == 1):
            chart = LineChart()
            chart.title = df['shortName'][0]
            chart.y_axis.title = 'price'
            chart.x_axis.title = 'time stamp'
            
            data = Reference(worksheet, min_col=2, min_row=2, max_col=7, max_row=dups_name)
            
            chart.add_data(data)
            
            worksheet.add_chart(chart, 'L4')
        else:
            i = 2
            j = 0
            for dup in dups_name:
                total_elems += dup
                
                chart = LineChart()
                chart.title = unique_names[j]
                j += 1
                
                chart.y_axis.title = 'price'
                chart.x_axis.title = 'time stamp'
                
                data = Reference(worksheet, min_col=2, min_row=i, max_col=7, max_row=total_elems+1)
                chart.add_data(data)
                
                worksheet.add_chart(chart, 'L'+str(i*4))
                i += dup
                
        writer.save()
        writer.close()
```
The first we do is call the previous method to create the excel files and then we make a dictionary using all the file names as values:
```py
to_xl()
excels = listdir('markets')
```
We're making a list of filenames because we're then going to iterate over these files.
We define the filepath and create our `ExcelWriter` object pointing to the excel file.
Generating a chart we first need to get the current worksheet. To do we load the workbook and all of the sheets into our `writer` variable. 
However, since there's only one sheet per file, we only care about the first index.
```py
for excel in excels:
    filepath = 'markets/' + excel
    writer = pd.ExcelWriter(filepath , engine='openpyxl')
    df = pd.read_excel(filepath)
    workbook = load_workbook(filepath)
    writer.book = workbook
        
    worksheet=writer.book.worksheets[0]
```
Now we need to address the problem of multiple contracts and duplicates. So I define a variable called `total_elems` and I've given it a value of `0`.
Again we have to parse the excel so we can get the number of duplicates and the values of unique elements.
```py
dups = df.pivot_table(index=['shortName'], aggfunc='size')
unique_names = df.shortName.unique()
```
Chart generation changes whether there are the same contracts in the data so we split them up using an `if` statement like so:
```py
if (len(dups_name) == 1):
    # Code Here

else:
    # More Code Here
```
The code in these statements is similar. 
When there is only one contract we do the following:
```py
chart = LineChart()
chart.title = df['shortName'][0]
chart.y_axis.title = 'price'
chart.x_axis.title = 'time stamp'
            
data = Reference(worksheet, min_col=2, min_row=2, max_col=7, max_row=dups_name)
            
chart.add_data(data)
            
worksheet.add_chart(chart, 'L4')
```
We create a `LineChart` object and we define the titles of the chart and of the axes. Next we have to fetch our data from the sheet. 
We do this with the `Reference` object. Here we must define what columns and rows will be used. Here the `max_row` is the number of duplicates.
We then add the data to chart and finally add the chart to the worksheet at the specified cell.

When there are more than just one type of contract, we generate the charts with the following code:
```py
i = 2
j = 0
for dup in dups:
    total_elems += dup
                
    chart = LineChart()
    chart.title = unique_names[j]
    j += 1
                
    chart.y_axis.title = 'price'
    chart.x_axis.title = 'time stamp'
                
    data = Reference(worksheet, min_col=2, min_row=i, max_col=7, max_row=total_elems+1)
    chart.add_data(data)
                
    worksheet.add_chart(chart, 'L'+str(i*4))
    i += dup
```
Here the variables `i` and `j` are used as index indicators. We loop through the number of unique duplicates to get the number of charts needed.
The variable instantiated before, `total_elems`, gets larger everytime the loop is run because it defines the maximum of rows used in the `Reference` object.
We define the many charts and give it a title that changes depending on the index of `unique_names`. We increment `j` by one.
Like before, titles for the axes are given. Next we create our `Reference` data. 
`min-row` is equal to `i` because this value will increase by the number of duplicates every loop. The same goes for `max_row`.
Again we add the data and add the chart to the worksheet.

Finally we `save` and `close` the `writer` object.

The data for this market is updated every minute or so. So, I've written a small script in `powershell` that only runs between business hours and every 60 seconds:
```ps1
write-host "Running"
[int] $hour = get-date -format HH
while ($hour -gt 8 -or $hour -lt 17) {
	py ./data_show.py;
    write-host "Done"
	start-sleep (60*1);
	./run.ps1
}
```

### IV. Problems Faced
When first starting to pull the data from the API, I didn't know how to process the information in `bytes`. I also didn't know if I wanted the data to be in `json` format or in another dictionary. I decided on `json` because I'm most familiar with it.
Another problem I faced was when I tried adding data to an existing sheet. Before I decided to separate the different markets into files, they were all in one file in separate sheets. This made the file way too big and I had issues with compression that I resolved by making different files. 
I also had an issue with data compression when charts remained in files. Because of the numerous charts, my files would get corrupted and nothing worked. Having the file deleted and then recreated erases all of the charts. There are definitely improvements that could be made; I wasn't able to define the series name in the charts nor use the `timeStamp` column as the x axis.

### V. Conclusion
Through this project I was able to get a better of `python` and automation. If possible I would want this program to evolve further pull data from other markets.

