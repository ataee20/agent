var page = require('webpage').create() ;
var login = 'http://localhost:2538/login.htm' ;
var home = 'http://localhost:2538/status.htm' ;

page.onConsoleMessage = function(msg) {
    console.log(msg);
};

page.onLoadFinished = function(){

    var html = page.evaluate(function(){
        return document.getElementsByTagName("*").length;
    });
    console.log(html);
    phantom.exit();

};  

page.open(login, function (status) {
    if (status !== 'success') {
        console.log('fail!');
        phantom.exit(1);
    } else {
        page.evaluate(function(){
            document.getElementById("username").value='admin';
            document.getElementById("password").value='asc@t185';
            document.getElementById("loginBtn").click()
        });

        
    }
});