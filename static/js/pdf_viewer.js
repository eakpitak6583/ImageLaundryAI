// ======================================================
// LaundryBot V7 Enterprise
// PDF Viewer Javascript
// Enterprise Edition
// ======================================================

pdfjsLib.GlobalWorkerOptions.workerSrc =
"https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.5.136/pdf.worker.min.js";

// ======================================================
// Config
// ======================================================

const pdfUrl = PDF_URL;

const searchKeyword =

(typeof SEARCH_KEYWORD === "string")

? SEARCH_KEYWORD.trim()

: "";

let pdfDoc = null;

let pageNum = Number(START_PAGE) || 1;

let scale = 1.4;

const canvas = document.getElementById("pdf_canvas");

const ctx = canvas.getContext("2d");

const loading = document.getElementById("loading");

// ======================================================

async function renderPage(page){

    if(!pdfDoc)
        return;

    pageNum = page;

    const pdfPage =
        await pdfDoc.getPage(page);

    const viewport =
        pdfPage.getViewport({

            scale

        });

    canvas.width = viewport.width;

    canvas.height = viewport.height;

    await pdfPage.render({

        canvasContext:ctx,

        viewport

    }).promise;

    document.getElementById("page_num").textContent = page;

    document.getElementById("page_input").value = page;

    document.getElementById("zoom_percent").textContent =
        Math.round(scale*100)+"%";

    await highlightKeyword(

        pdfPage,

        viewport

    );

}

// ======================================================

async function highlightKeyword(pdfPage){

    if(searchKeyword==="")
        return;

    try{

        const text =
            await pdfPage.getTextContent();

        const full =
            text.items
            .map(x=>x.str)
            .join(" ")
            .toLowerCase();

        if(

            full.includes(

                searchKeyword.toLowerCase()

            )

        ){

            console.log(

                "Found :",searchKeyword

            );

        }

    }

    catch(err){

        console.error(err);

    }

}

// ======================================================

async function loadPDF(){

    try{

        pdfDoc =
            await pdfjsLib
            .getDocument(pdfUrl)
            .promise;

        document.getElementById(

            "page_count"

        ).textContent = pdfDoc.numPages;

        if(pageNum<1)
            pageNum=1;

        if(pageNum>pdfDoc.numPages)
            pageNum=pdfDoc.numPages;

        await renderPage(pageNum);

    }

    catch(err){

        console.error(err);

        alert("ไม่สามารถเปิด PDF");

    }

    finally{

        if(loading){

            loading.style.display="none";

        }

    }

}

// ======================================================

function nextPage(){

    if(pageNum>=pdfDoc.numPages)
        return;

    renderPage(pageNum+1);

}

function prevPage(){

    if(pageNum<=1)
        return;

    renderPage(pageNum-1);

}

function jumpPage(){

    let p=parseInt(

        document.getElementById(

            "page_input"

        ).value

    );

    if(isNaN(p))
        return;

    if(p<1)
        p=1;

    if(p>pdfDoc.numPages)
        p=pdfDoc.numPages;

    renderPage(p);

}

// ======================================================

function zoomIn(){

    scale+=0.2;

    renderPage(pageNum);

}

function zoomOut(){

    if(scale<=0.6)
        return;

    scale-=0.2;

    renderPage(pageNum);

}

function fitWidth(){

    const viewer =

        document.querySelector(".viewer");

    scale =

        (viewer.clientWidth-80)

        / canvas.width

        * scale;

    renderPage(pageNum);

}

// ======================================================

function toggleFullscreen(){

    if(!document.fullscreenElement){

        document.documentElement.requestFullscreen();

    }

    else{

        document.exitFullscreen();

    }

}

// ======================================================

window.addEventListener(

    "keydown",

    e=>{

        if(e.key==="ArrowRight")

            nextPage();

        if(e.key==="ArrowLeft")

            prevPage();

    }

);

// ======================================================

window.addEventListener(

    "wheel",

    e=>{

        if(!e.ctrlKey)
            return;

        e.preventDefault();

        if(e.deltaY<0)

            zoomIn();

        else

            zoomOut();

    },

    {

        passive:false

    }

);

// ======================================================

window.addEventListener(

    "resize",

    ()=>{

        if(pdfDoc)

            renderPage(pageNum);

    }

);

// ======================================================

window.addEventListener(

    "load",

    loadPDF

);