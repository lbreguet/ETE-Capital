let getXMLFile = (path, callback) => {
    let request = new XMLHttpRequest()
    request.open('GET', path)
    request.setRequestHeader('Content-Type', 'text/xml')
    request.onreadystatechange = () => {
        if (request.readyState === 4 && request.status === 200) {
            callback(request.responseXML)
        }
    }
    request.send()
}

getXMLFile('https://www.predictit.org/api/marketdata/all', function (xml) {
    console.log(xml)
})