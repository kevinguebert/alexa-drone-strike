(function() {

    var xmlHTTP = new XMLHttpRequest();

    console.log('here');
    xmlHTTP.open("GET", 'http://api.dronestre.am/data', false);
    xmlHTTP.send(null);
    console.log(xmlHTTP);
    console.log(xmlHTTP.resposneText);
    //     if(!error && response.status == "OK") {
    //         //Successful request
    //         var strikes      = body.strikes;
    //         var totalStrikes = strikes.length;
    //         var mostRecent   = strikes[strikes.length-1];
    //
    //
    //         var strikeSpeechOutput = mostRecent.narrative;
    //         this.emit(':tellWithCard', strikeSpeechOutput, this.t("SKILL_NAME"), mostRecent.narrative);
    //     } else if(error) {
    //
    //     }
    //
    // });
})();
