'use strict';

var mediasearch = angular.module(
  'Mediasearch',
  [
    'btford.socket-io'
  ]
);

mediasearch.service(
  'results',
  function(){

    var _items = [ ];
    var _done = false;

    function reset(){
      _items = [ ];
      _done = false;
    }

    function append(item){
      _items.push(item);
    }

    function done(){
      _done = true;
    }

    function is_done(){
      return _done;
    }

    function length(){
      return _items.length;
    }

    function items(){
      return _items;
    }

    var self = {
      items: items,
      reset: reset,
      append: append,
      done: done,
      is_done: is_done,
      length: length
    };

    return self;

  }
);

mediasearch.config(
  function(socketProvider){

    var search_socket = io.connect('/search');

    socketProvider.ioSocket(search_socket);

  }
);

function MediasearchForm($scope, socket, results){

    var form = {
      search_query: ''
    };

    $scope.form = form;

    $scope.search = function(){

      var search_query = form.search_query;

      console.log('searching for query [%s]', search_query);

      results.reset();

      socket.emit('search', search_query);

    };

}

function MediasearchResultsController($scope, socket, results){

  $scope.items = [ ];
  $scope.count = 0;

  function update_results(){
    console.log('updating results');

    var count = results.length();
    $scope.count = count;
    $scope.results_visible = count > 0;
    $scope.results_done = results.is_done();
    $scope.items = results.items();

    console.log('there are %d results', count);
  }

  socket.on(
    'result',
    function(data){
      results.append(data);
      $scope.$apply(update_results);
    }
  );

  socket.on(
    'done',
    function(data){
      results.done();
      $scope.$apply(update_results);
      console.log('done with search [%s]', data);
    }
  );

  update_results();

}

mediasearch.controller(
  'MediasearchForm',
  ['$scope', 'socket', 'results', MediasearchForm]
);

mediasearch.controller(
  'MediasearchResultsController',
  ['$scope', 'socket', 'results', MediasearchResultsController]
);
