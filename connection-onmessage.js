
 connection.onmessage = function(event) {
        var newData = JSON.parse(event.data);
        var updateObject =[{
            "Name": newData.Name,
            "Year": newData.Year,
            "Spent": newData.Spent,
            "payType": newData.payType
        }]
        //resetData(ndx, [yearDim, spendDim, nameDim]);
        xfilter.add(updateObject);
        dc.redrawAll();
    }