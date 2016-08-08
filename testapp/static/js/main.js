var app =angular.module('testapp', ['ngRoute', 'ui.bootstrap'])
.config(['$locationProvider', '$httpProvider', function($locationProvider, $httpProvider) {
    $locationProvider.html5Mode(true);
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
}])
.controller('TestAppController', ['$scope', '$http', '$location', function($scope, $http, $location) {
  // $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  var controller = this;

  controller.stockLists = [];
  controller.filterForm = {};
  controller.filterForm.radio = "none";


  controller.totalItems = controller.stockLists.length;
  controller.currentPage = 1;
  controller.itemsPerPage =  10;
  controller.numPages = 5; 
  controller.maxSize = 5;//Number of pager buttons to show
  controller.isFilterApplied = false;

  controller.sortType     = 'id'; // set the default sort type
  controller.sortReverse  = false;  // set the default sort order


  controller.today = function() {
    controller.filterForm.dateTo = new Date();
    controller.filterForm.dateFrom = new Date();
  };

  controller.today();
  controller.inlineOptions = {
    customClass: getDayClass,
    minDate: new Date(),
    showWeeks: true
  };

  controller.dateOptions = {
    dateDisabled: disabled,
    formatYear: 'yy',
    maxDate: new Date(2020, 5, 22),
    minDate: new Date(),
    startingDay: 1
  };

  // Disable weekend selection
  function disabled(data) {
    var date = data.date,
      mode = data.mode;
    return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
  }

  function getDayClass(data) {
    var date = data.date,
      mode = data.mode;
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);

      for (var i = 0; i < $scope.events.length; i++) {
        var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return $scope.events[i].status;
        }
      }
    }

    return '';
  }

  controller.format = "dd-MM-yyyy";
  controller.altInputFormats = ['M!/d!/yyyy'];

  controller.popup1 = {
    opened: false
  };

  controller.popup2 = {
    opened: false
  };

  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  controller.toggleMin = function() {
    controller.inlineOptions.minDate = controller.inlineOptions.minDate ? null : new Date();
    controller.dateOptions.minDate = controller.inlineOptions.minDate;
  };

  controller.toggleMin();

  controller.open1 = function() {
    controller.popup1.opened = true;
  };

  controller.open2 = function() {
    controller.popup2.opened = true;
  };

  controller.pageChanged = function() {
    if (controller.isFilterApplied) {
      controller.getData(controller.currentPage, controller.itemsPerPage, $.param(controller.filterForm));
    } else {
      controller.getData(controller.currentPage, controller.itemsPerPage, null);
    }
  };

  controller.resetFilter = function () {
    controller.today();
    controller.filterForm.radio = "none";
    controller.isFilterApplied = false;

    controller.getData(1, controller.itemsPerPage, null, controller.sortType, controller.sortReverse);
  }

  controller.filterFormSubmit = function() {
    controller.isFilterApplied = true;
    controller.currentPage = 1;
    filters = $.param(controller.filterForm);
    controller.getData(1, controller.itemsPerPage, filters);
  }

  controller.sort = function(sorttype) {
    controller.sortReverse = !controller.sortReverse;
    controller.sortType = sorttype;

    controller.currentPage = 1;

    if (controller.isFilterApplied) {
      controller.getData(1, controller.itemsPerPage, $.param(controller.filterForm), sorttype, controller.sortReverse);
    } else {
      controller.getData(1, controller.itemsPerPage, null, sorttype, controller.sortReverse);
    }
  }

  controller.getData = function(page = 1, itemsPerPage = controller.itemsPerPage, formData=null, sort=controller.sortType, sortreverse=controller.sortReverse) {
    var postData = 'page=' + page + '&itemsPerPage=' + itemsPerPage + '&filters=' + formData+ '&sort=' + sort + '&sortreverse=' + sortreverse;

    $http({
      method : "post",
      url : "/getData",
      data : postData
    }).then(function mySucces(responseData) {
        controller.totalItems = responseData.data.count;
         var stockDatas = JSON.parse(responseData.data.data);

        controller.stockLists = [];
        angular.forEach(stockDatas, function(value, key) {
          data = stockDatas[key].fields;
          controller.stockLists.push(data);
        }, []);
    }, function myError(response) {
      console.log('Error: ' + response);
    });
  };
  controller.getData(1);
}]);
