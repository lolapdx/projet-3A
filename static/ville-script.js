const currentUrl = window.location.href;
const villeName = currentUrl.split("/villes/")[1];


const grid = document.querySelector(".grid");

const hier = new Date();
hier.setTime(hier.getTime() - 24 * 3600 * 1000);
const jour_hier = hier.toISOString().substring(0,11) + '00:00:00Z';
// hier.setHours(0, 0, 0, 0);

function formatLisible(date){
    let date_mois=date.substring(5,7);
    let date_jour=date.substring(8,10);
    let date_annee=date.substring(0,4);
    return date_jour + '/' + date_mois + '/' + date_annee;
}


console.log(villeName);
console.log(jour_hier);

const oeuvre_du_jour = document.querySelector("#oeuvre_jour");
const nom_ville_jour = document.querySelector("#nom_ville_jour");
const nom_ville_annee = document.querySelector("#nom_ville_annee");

nom_ville_annee.textContent = villeName + ' 2024';


function fetchGrandeImage(date){
    console.log("date demandée :", date);
    oeuvre_du_jour.innerHTML='Chargement...';
    fetch("/villes/" + villeName.toLowerCase() + "/jour/" + date)
        .then(response => response.blob())
        .then(blob => {
            oeuvre_du_jour.innerHTML='';
            let img_jour = document.createElement('img');
            let url_jour = URL.createObjectURL(blob);
            img_jour.src = url_jour;
            oeuvre_du_jour.appendChild(img_jour);
            nom_ville_jour.textContent = villeName + ' ' + formatLisible(date);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }


fetchGrandeImage(jour_hier);


//Création du tableau à l'année

const monthsLetters=["J","F","M","A","M","J","J","A","S","O","N","D"]

function buildDay(id){
    let day = document.createElement("div");
    day.classList.add("circle");
    day.setAttribute("day-id",id);
    let day_img = document.createElement("img");
    let date_mois=id.substring(5,7).padStart(2, '0');
    let date_jour=id.substring(8,10).padStart(2, '0');
    var source = "../static/images/"+villeName.toLowerCase()+"/"+villeName.toLowerCase()+"_2024_"+date_mois+"_"+date_jour+".png";
    day_img.src = source ;
    day.appendChild(day_img);
    day.addEventListener('click', () => fetchGrandeImage(id));
    return day;
}

function buildDayNumber(day){
    let dayNumber = document.createElement("div");
    dayNumber.classList.add("date");
    let dayNumber_img = document.createElement("img");
    let day_formatted = day.toString().padStart(2, '0');
    dayNumber_img.src = "../static/images/tableau_annee/"+day_formatted+".png";
    dayNumber.appendChild(dayNumber_img);
    return dayNumber;
}


function displayYear(){
    //premier vide
    let day0=document.createElement("div");
    day0.classList.add("circle");
    grid.appendChild(day0)

    //premiere ligne
    for (let day=1;day < 32; day++) {
        let dayNumber = buildDayNumber(day);
        grid.appendChild(dayNumber);
    }

    //Reste du tableau
    for (let month=0; month < 12; month++) {

         //début de ligne --> lettre du mois
         let monthLetter = document.createElement("div");
         monthLetter.classList.add("date");
         let monthLetter_img = document.createElement("img");
         monthLetter_img.src = "../static/images/tableau_annee/"+monthsLetters[month]+".png";
         monthLetter.appendChild(monthLetter_img);
         grid.appendChild(monthLetter);

         //suivi des images
        for (let d = 1; d < 32; d++) {
            let id = generateDate(d, month);
            // console.log(id)
            if (id==='Date invalide'){
                let jour_vide=document.createElement("div");
                jour_vide.classList.add("circle");
                grid.appendChild(jour_vide)
            }
            else{
                let day = buildDay(id);
                grid.appendChild(day);  
            }
        }
    }
}

function generateDate(d, month) {
    var year = 2024;
    var month = month; // Les mois sont indexés à partir de 0 (janvier = 0)
    var day = d;
    if (isValidDate(year,month, day)){
        var date = new Date(Date.UTC(year, month, day));
        date = date.toISOString().substring(0,11) + '00:00:00Z';   // Formate la date en "YYYY-MM-DDTHH:MM:SSSZ"
        return date;
    }
    else { return ("Date invalide") }
}

function isValidDate(year, month, day) {
    var date = new Date(Date.UTC(year, month, day));
    return date.getUTCFullYear() === year &&
           date.getUTCMonth() === month &&
           date.getUTCDate() === day;
}


displayYear()