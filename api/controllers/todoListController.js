'use strict';

var count = 0;


var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
var regex = new RegExp(expression);



var mongoose = require('mongoose'),
  Task = mongoose.model('Tasks');

exports.list_all_tasks = function(req, res) {
  Task.find({}, function(err, task) {
    if (err)
      res.send(err);
    res.json(task);
  });
};




exports.create_a_task = function(req, res) {
  var new_task = new Task(req.body);
  if (req.body.short == null) {
    new_task.short = count++;
  }
  if (! req.body.name.match(regex)) {
    res.status(400)
    res.send(err);
  }
  new_task.save(function(err, task) {
    if (err)
      res.send(err);
    res.status(201);
    res.json(task);
  });
};

/*
exports.read_a_task = function(req, res) {
  Task.findById(req.params.taskId, function(err, task) {
    if (err)
      res.send(err);
    res.json(task);
  });
};*/

exports.read_a_task = function(req, res) {
  Task.findOne({short: req.params.taskId}, function(err, task) {
    if (err)
      res.send(err);
    else if(task == null){
      res.status(404);
      res.send(err);
    } else {
      res.status(301);
      res.redirect(301, "http://" + task.name);
    }
  });
};


exports.update_a_task = function(req, res) {
  Task.findOneAndUpdate({short: req.params.taskId}, req.body, {new: true}, function(err, task) {
    if (err)
      res.send(err);
    else if (! req.body.name.match(regex)) {
      res.status(400)
      res.send(err);
    }
    else if(task == null){
      res.status(404);
      res.send(err);
    }else{
      res.json(task);
    }
  });
};


exports.delete_a_task = function(req, res) {
  // We had to add this so that it would return 404 if not found
  Task.findOne({short: req.params.taskId}, function(err, task) {
    if (err)
      res.send(err);
    else if(task == null){
      res.status(404);
      res.send(err);
    }else{
      Task.deleteOne({
        short: req.params.taskId
      }, function(err, task) {
        if (err) {
          res.send(err);
        } else {
          res.status(204);
          res.json({ message: 'Task successfully deleted' });
        }
      });
    }
  });


};

exports.delete_all_task = function(req, res) {

  Task.deleteMany({}, function(err, task) {
    if (err)
      res.send(err);
    res.status(204);
    res.json({ message: 'Tasks successfully deleted' });
  });
};


