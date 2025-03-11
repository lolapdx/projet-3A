// ici pas clair si hier est bien hier...
const hier = new Date();
console.log(hier);
hier.setTime(hier.getTime() - 24 * 3600 * 1000);
console.log(hier);
const jour_hier = hier.toISOString().substring(0,11) + '00:00:00Z'; //a priori ca pourrait faire le jour de avant encore
console.log(jour_hier);

const oeuvre_Nantes = document.querySelector("#oeuvre_Nantes");
const oeuvre_Marseille = document.querySelector("#oeuvre_Marseille");
const oeuvre_Lille = document.querySelector("#oeuvre_Lille");
const oeuvre_Paris = document.querySelector("#oeuvre_Paris");
const oeuvre_Lyon = document.querySelector("#oeuvre_Lyon");

function fetch_images(jour) {
    oeuvre_Nantes.innerHTML = "chargement...";
    oeuvre_Marseille.innerHTML = "chargement...";
    oeuvre_Lille.innerHTML = "chargement...";
    oeuvre_Paris.innerHTML = "chargement...";
    oeuvre_Lyon.innerHTML = "chargement...";
    fetch("/jour/" + jour)
        .then(response => response.json())
        .then(data => {
            console.log("data fetched");

            oeuvre_Nantes.innerHTML = "";
            oeuvre_Marseille.innerHTML = "";
            oeuvre_Lille.innerHTML = "";
            oeuvre_Paris.innerHTML = "";
            oeuvre_Lyon.innerHTML = "";

            const img_marseille = document.createElement('img');
            img_marseille.src = data.marseille;
            oeuvre_Marseille.appendChild(img_marseille);

            const img_paris = document.createElement('img');
            img_paris.src = data.paris;
            oeuvre_Paris.appendChild(img_paris);

            const img_lyon = document.createElement('img');
            img_lyon.src = data.lyon;
            oeuvre_Lyon.appendChild(img_lyon);

            const img_nantes = document.createElement('img');
            img_nantes.src = data.nantes;
            oeuvre_Nantes.appendChild(img_nantes);

            const img_lille = document.createElement('img');
            img_lille.src = data.lille;
            oeuvre_Lille.appendChild(img_lille);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

fetch_images(jour_hier);


    
// Calendar

document.addEventListener('DOMContentLoaded', function(){
    var today = new Date(),
        year = today.getFullYear(),
        month = today.getMonth(),
        monthTag =["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        day = today.getDate(),
        days = document.getElementsByTagName('td'),
        selectedDay,
        setDate,
        daysLen = days.length;
// options should like '2014-01-01'
    function Calendar(selector, options) {
        this.options = options;
        this.draw();
    }
    
    Calendar.prototype.draw  = function() {
        this.getCookie('selected_day');
        this.getOptions();
        this.drawDays();
        var that = this,
            reset = document.getElementById('reset'),
            pre = document.getElementsByClassName('pre-button'),
            next = document.getElementsByClassName('next-button');
            
            pre[0].addEventListener('click', function(){that.preMonth(); });
            next[0].addEventListener('click', function(){that.nextMonth(); });
            reset.addEventListener('click', function(){that.reset(); });
        while(daysLen--) {
            days[daysLen].addEventListener('click', function(){that.clickDay(this); });
        }
    };
    
    Calendar.prototype.drawHeader = function(e) {
        var headDay = document.getElementsByClassName('head-day'),
            headMonth = document.getElementsByClassName('head-month');

            e?headDay[0].innerHTML = e : headDay[0].innerHTML = day;
            headMonth[0].innerHTML = monthTag[month] +" - " + year;        
        };
    
    Calendar.prototype.drawDays = function() {
        var startDay = new Date(year, month, 1).getDay(),
            nDays = new Date(year, month + 1, 0).getDate(),
    
            n = startDay;
        for(var k = 0; k <42; k++) {
            days[k].innerHTML = '';
            days[k].id = '';
            days[k].className = '';
        }

        for(var i  = 1; i <= nDays ; i++) {
            days[n].innerHTML = i; 
            n++;
        }
        
        for(var j = 0; j < 42; j++) {
            if(days[j].innerHTML === ""){
                
                days[j].id = "disabled";
                
            }else if(j === day + startDay - 1){
                if((this.options && (month === setDate.getMonth()) && (year === setDate.getFullYear())) || (!this.options && (month === today.getMonth())&&(year===today.getFullYear()))){
                    this.drawHeader(day);
                    days[j].id = "today";
                }
            }
            if(selectedDay){
                if((j === selectedDay.getDate() + startDay - 1)&&(month === selectedDay.getMonth())&&(year === selectedDay.getFullYear())){
                days[j].className = "selected";
                this.drawHeader(selectedDay.getDate());
                }
            }
        }
    };
    
    Calendar.prototype.clickDay = function(o) {
        console.log(o);
        var selected = document.getElementsByClassName("selected"),
            len = selected.length;
        if(len !== 0){
            selected[0].className = "";
        }
        o.className = "selected";
        selectedDay = new Date(year, month, o.innerHTML);
        let selectedDate = selectedDay;
        selectedDate.setTime(selectedDate.getTime() + 24 * 3600 * 1000);

        console.log("selected day:", selectedDay);
        this.drawHeader(o.innerHTML);
        this.setCookie('selected_day', 1);
        
        selectedDate = selectedDay.toISOString().substring(0, 11) + '00:00:00Z';
        console.log("selectedDate:", selectedDate);
        fetch_images(selectedDate);
    };
    
    Calendar.prototype.preMonth = function() {
        if(month < 1){ 
            month = 11;
            year = year - 1; 
        }else{
            month = month - 1;
        }
        this.drawHeader(1);
        this.drawDays();
    };
    
    Calendar.prototype.nextMonth = function() {
        if(month >= 11){
            month = 0;
            year =  year + 1; 
        }else{
            month = month + 1;
        }
        this.drawHeader(1);
        this.drawDays();
    };
    
    Calendar.prototype.getOptions = function() {
        if(this.options){
            var sets = this.options.split('-');
                setDate = new Date(sets[0], sets[1]-1, sets[2]);
                day = setDate.getDate();
                year = setDate.getFullYear();
                month = setDate.getMonth();
        }
    };
    
        Calendar.prototype.reset = function() {
            month = today.getMonth();
            year = today.getFullYear();
            day = today.getDate();
            this.options = undefined;
            this.drawDays();
        };
    
    Calendar.prototype.setCookie = function(name, expiredays){
        if(expiredays) {
            var date = new Date();
            date.setTime(date.getTime() + (expiredays*24*60*60*1000));
            var expires = "; expires=" +date.toGMTString();
        }else{
            var expires = "";
        }
        document.cookie = name + "=" + selectedDay + expires + "; path=/";
    };
    
    Calendar.prototype.getCookie = function(name) {
        if(document.cookie.length){
            var arrCookie  = document.cookie.split(';'),
                nameEQ = name + "=";
            for(var i = 0, cLen = arrCookie.length; i < cLen; i++) {
                var c = arrCookie[i];
                while (c.charAt(0)==' ') {
                    c = c.substring(1,c.length);
                    
                }
                if (c.indexOf(nameEQ) === 0) {
                    selectedDay =  new Date(c.substring(nameEQ.length, c.length));
                }
            }
        }
    };
    var calendar = new Calendar();
    
        
}, false);