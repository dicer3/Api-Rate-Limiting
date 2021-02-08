    var str=window.location.search;//Retrving parameters in URL
    var count=0;
    var CurrStr;
    var EmailId,ThRoute1,ThRoute2;
    // Finding values of Thersolds of Both the Routes
    for(var i=1;i<str.length;i++)
    {    
        if(count==2 && str[i]=='&')
            ThRoute1=CurrStr;
        if(count==1 && str[i]=='&')
            EmailId=CurrStr;
        CurrStr+=str[i];
        if(str[i]=='=')
        {
            CurrStr=' ';
            count++;
        }
    }
    ThRoute2=CurrStr;
    reset=true
    /* 
       wrapping message as JSON object
       and inserting the values of Thersolds
       of routes and reset value
       they are retrieved when recieved from server 
    */
    let message=
    {
        ThDevRoute:ThRoute1,
        ThOrgRoute:ThRoute2,
        reset:reset
    }
    function DevRequest()
    {                    
        // sending POST request to developers route                                                                 
        $.post("http://127.0.0.1:5000/developers",JSON.stringify(message),function(response){
            document.getElementById('DevAnswerDisplay').innerHTML =response;//if request was successful then write the response
            document.getElementById('DevAnswerDisplay').style.color='#ADFF2F'; 
            console.log(response)
        }).fail(function(){
           document.getElementById('DevAnswerDisplay').innerHTML ="Request Limit Exceeded";// else if limit exceeds write limit exceeded
           document.getElementById('DevAnswerDisplay').style.color='#DC143C'; 
        });
        document.getElementById('DevAnswerDisplay').innerHTML="";//make it empty so that it could be written when next request is made
        message.reset=false;
    }
    function OrgRequest()
    {
        // sending POST request to organisations route
        $.post("http://127.0.0.1:5000/organisations",JSON.stringify(message),function(response){
            document.getElementById('OrgAnsDisplay').innerHTML =response;//if request was successful then write the response
            document.getElementById('OrgAnsDisplay').style.color='#ADFF2F'; 
            console.log(response)
        }).fail(function(){
           document.getElementById('OrgAnsDisplay').innerHTML ="Request Limit Exceeded";// else if limit exceeds write limit exceeded 
           document.getElementById('OrgAnsDisplay').style.color='#DC143C';
        });   
        document.getElementById('OrgAnsDisplay').innerHTML="";//make it empty so that it could be written when next request is made
        message.reset=false;
    }