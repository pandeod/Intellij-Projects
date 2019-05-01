$(document).ready(function(e){

    localStorage['uploadedFileName']='';

    $("#upload_file").click(function(e){
        var form_data = new FormData($('#file_form')[0]);
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            cache: false,
            processData:false,
            success: function(data){
                if(data.status=='200'){
                    console.log("File Uploaded Successfully status: "+data.result);
                    console.log("No. of sentences in file : "+data.length);
                    localStorage['uploadedFileName']=data.result;
                    $('#upload_file').attr('disabled',true);
                    $('#summarize_btn').attr('disabled',false);
                    $('#cancel-selected-file').show();
                    confirm("Your file has been uploaded..\nNo. of Sentences detected : "+data.length);
                }else{
                    $('#file_form')[0].reset();
                    $("#custom-text").text('Choose File');
                    $('#cancel-selected-file').hide();
                    console.log("Error occurred  status:"+data.status);
                    alert("ERROR !!!");
                }
                $('#file_form').css("opacity","");
            },
            error:function(err){
                $('#file_form')[0].reset();
                $("#custom-text").text('Choose File');
                $('#cancel-selected-file').hide();
                console.log("Failed Request  status:"+err.status);
                alert(err.status);
                $('#upload_file').attr('disabled',true);
            }
        });
    });

    //cancel selected file
    $('#cancel-selected-file').click(function () {
        var filename=localStorage['uploadedFileName'];
        $.ajax({
            type:'POST',
            url:'/closesummary',
            data:filename,
            contentType:false,
            cache:false,
            processData:false,
            success: function (data) {
                if(data.status=='200')
                {
                    localStorage['uploadedFileName']='';
                    console.log(data['response']);
                    $("#file").val('');
                    $("#custom-text").text('Choose File');
                    $('#cancel-selected-file').hide();
                    $('#upload_file').attr('disabled',true);
                    // $('#summarize_btn').attr('disabled',true);
                }
                else
                    console.log('Failed to delete file')
            },
            error: function (err) {
                console.log(err.status);
            }
        });
    });

    // $('#textBox').onchange(function () {
    //     var str=$('#textBox').val();
    //     var len=str.trim().length;
    //     if(len>1)
    //     {
    //         $('#summarize_btn').attr('disabled',false);
    //     }
    //     else
    //     {
    //         $('#summarize_btn').attr('disabled',true);
    //     }
    // });

    //modal text display
    $("#summarize_btn").click(function(){
        var filename=localStorage['uploadedFileName'];
        $("#summaryBox").text("Loading your summary ...........");
        var length=$('#inputLength').val();
        if(length == null)
            length=1;
        if(filename=='')
        {
            alert('You are sending text input')
            var input_text=$('#textBox').val();
            d={'input_text':input_text,'sumLen':length}
            $.ajax({
                type:'POST',
                url:'/requestsummarybybox',
                data: JSON.stringify(d),
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                processData:false,
                success: function (data) {
                    var responseSummary=data['summary']
                    $("#summaryBox").text(responseSummary+"");
                },
                error: function (err) {
                    console.log(err.status);
                }
            });
        }
        else
        {
            d={'fname':filename,'sumLen':length}
            $.ajax({
                type: 'POST',
                url: '/requestsummary',
                data: JSON.stringify(d),
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                processData:false,
                success: function (data) {
                    var responseSummary=data['summary']
                    $("#summaryBox").text(responseSummary+"");
                },
                error: function (err) {
                    console.log(err.status);
                }
            });
        }
    });

    //remove modal display
    $("#close-modal").click(function(){
        var filename=localStorage['uploadedFileName'];
        $.ajax({
            type: 'POST',
            url: '/closesummary',
            data: filename,
            contentType: false,
            cache: false,
            processData:false,
            success: function (data) {
                if(data.status=='200')
                {
                    localStorage['uploadedFileName']='';
                    console.log(data['response']);
                    $("#summaryBox").text('');
                    $("#textBox").text('');
                    $("#file").val('');
                    $("#custom-text").text('Choose File');
                    $('#cancel-selected-file').hide();
                    $('#upload_file').attr('disabled',true);
                    // $('#summarize_btn').attr('disabled',true);
                }
                else
                    console.log('Failed to delete file')
            },
            error: function (err) {
                console.log(err.status);
            }
        });
    });

    // $("#switch-button").change(function () {
    //     if($("#switch-button").prop("checked")==true)
    //     {
    //         $('#upload_file').attr('disabled',true);
    //         $('#summarize_btn').attr('disabled',false);
    //     }
    //     else
    //     {
    //         $('#upload_file').attr('disabled',false);
    //         $('#summarize_btn').attr('disabled',true);
    //     }
    // });

    //file type validation
    $("#file").change(function() {
        var file = this.files[0];
        var inputFileType = file.type;
        var inputFileName = file.name;
        var fileSize = parseFloat(file.size / (1024*1024)).toFixed(2);
        var match= ["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","text/plain"];
        if(!((inputFileType==match[0]) || (inputFileType==match[1]) || (inputFileType==match[2]))){
            alert('Please select a valid file format');
            $("#file").val('');
            $("#custom-text").text('Choose File');
            return false;
        }
        if(fileSize>10){
            alert('Please select a valid file within 10MB');
            $("#file").val('');
            $("#custom-text").text('Choose File');
            return false;
        }
        $('#upload_file').attr('disabled',false);
        // $('#summarize_btn').attr('disabled',true);
        $('#custom-text').text(inputFileName.toString().substring(0,15));
    });

    document.getElementById("download_summary").onclick = function() {
        //when clicked the button
        var content = document.getElementById('summaryBox').value;

        var documentType=document.getElementById('menuFileType');
        var v=documentType.options[documentType.selectedIndex].value;

        switch(v)
        {
            case 'txt' : Export2Txt(content.toString());
                break;
            case 'pdf' : printPDF(content.toString());
                break;
            case 'doc' : Export2Doc(content.toString());
                break;
            default : Export2Txt(content.toString());
        }

        // var filename=localStorage['uploadedFileName'];
        // $.ajax({
        //     type: 'POST',
        //     url: '/getfile',
        //     data: filename,
        //     contentType: false,
        //     cache: false,
        //     processData:false,
        //     success: function (data) {
        //         console.log(data.status);
        //     },
        //     error: function (err) {
        //         console.log(err.status);
        //     }
        // });
    }

    function Export2Txt(text) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', "summary.txt");

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();
        document.body.removeChild(element);
    }

    function printPDF(text) {

        var lMargin=15; //left margin in mm
        var rMargin=15; //right margin in mm
        var pdfInMM=210;  // width of A4 in mm

        var pdf = new jsPDF("p","mm","a4");

        var lines =pdf.splitTextToSize(text, (pdfInMM-lMargin-rMargin));
        pdf.text(lMargin,20,lines);

        pdf.save('Summary.pdf');

        // var options = {
        //         pagesplit: true
        //     };

        // pdf.fromHTML(source, options, function()
        // {
        //     pdf.save("Summary.pdf");
        // });

        // var preHtml = "<html><head><meta charset='utf-8'><title>Summary</title></head><body>";
        // var postHtml = "</body></html>";
        // var source = preHtml+text+postHtml;


        // margins = {
        //     top: 0,
        //     bottom: 0,
        //     left: 0,
        //     width: 512
        // };

        // pdf.fromHTML(
        //     source, // HTML string or DOM elem ref.
        //     margins.left, // x coord
        //     margins.top, { // y coord
        //         'width': margins.width, // max width of content on PDF
        //     },function (dispose) {
        //         // dispose: object with X, Y of the last line add to the PDF
        //         //          this allow the insertion of new lines after html
        //         // save the PDF document (downloadable)
        //         pdf.save('Summary.pdf');
        //     }, margins);
    }

    function Export2PDF(text){
        var preHtml = "<html><head><meta charset='utf-8'><title>Summary</title></head><body>";
        var postHtml = "</body></html>";
        var html = preHtml+text+postHtml;

        var blob = new Blob(['\ufeff', html], {
            type: 'application/pdf'
        });

        // Specify link url
        var url = 'data:application/pdf;charset=utf-8,' + encodeURIComponent(html);

        // Specify file name
        filename = 'summary.pdf';

        // Create download link element
        var downloadLink = document.createElement("a");

        document.body.appendChild(downloadLink);

        if(navigator.msSaveOrOpenBlob ){
            navigator.msSaveOrOpenBlob(blob, filename);
        }else{
            // Create a link to the file
            downloadLink.href = url;

            // Setting the file name
            downloadLink.download = filename;

            //triggering the function
            downloadLink.click();
        }
        document.body.removeChild(downloadLink);
    }

    function Export2Doc(text){
        var preHtml = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'><head><meta charset='utf-8'><title>Summary</title></head><body>";
        var postHtml = "</body></html>";
        var html = preHtml+text+postHtml;

        var blob = new Blob(['\ufeff', html], {
            type: 'application/msword'
        });

        // Specify link url
        var url = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(html);

        // Specify file name
        filename = 'summary.doc';

        // Create download link element
        var downloadLink = document.createElement("a");

        document.body.appendChild(downloadLink);

        if(navigator.msSaveOrOpenBlob ){
            navigator.msSaveOrOpenBlob(blob, filename);
        }else{
            // Create a link to the file
            downloadLink.href = url;

            // Setting the file name
            downloadLink.download = filename;

            //triggering the function
            downloadLink.click();
        }
        document.body.removeChild(downloadLink);
    }

});