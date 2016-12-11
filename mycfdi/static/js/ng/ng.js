var angularApp = angular.module('myCFDI', ['ngResource']);

angularApp.controller('cfdiXMLUploadView' , [ '$scope' , '$resource' , cfdiXMLUploadView ]).config(function($httpProvider) {
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $httpProvider.defaults.headers.post['X-CSRFToken'] = token;
});


function cfdiXMLUploadView($scope , $resource){


       // GET THE FILE INFORMATION.
        $scope.getFileDetails = function (e) {

            $scope.files = [];
            $scope.$apply(function () {

                // STORE THE FILE OBJECT IN AN ARRAY.
                for (var i = 0; i < e.files.length; i++) {
                    $scope.files.push(e.files[i])
                }

            });
        };

        // NOW UPLOAD THE FILES.
        $scope.uploadFiles = function () {

            //FILL FormData WITH FILE DETAILS.
            var data = new FormData();
            var token = $('input[name=csrfmiddlewaretoken]').val();
            data.append("csrfmiddlewaretoken", token);

            for (var i in $scope.files) {
                data.append("uploadedFile", $scope.files[i]);
            }

            // ADD LISTENERS.
            var objXhr = new XMLHttpRequest();
            objXhr.addEventListener("progress", updateProgress, false);
            objXhr.addEventListener("load", transferComplete, false);

            // SEND FILE DETAILS TO THE API.
            objXhr.open("POST", "/REST/cfdi/xml/upload/");
            objXhr.send(data);
        }

        // UPDATE PROGRESS BAR.
        function updateProgress(e) {
            if (e.lengthComputable) {
                document.getElementById('pro').setAttribute('value', e.loaded);
                document.getElementById('pro').setAttribute('max', e.total);
            }
        }

        // CONFIRMATION.
        function transferComplete(e) {
            alert("Files uploaded successfully.");
        }
}