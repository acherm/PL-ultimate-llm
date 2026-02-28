# Simple Greeting App in EmberScript
App = Ember.Application.create()

App.Person = Ember.Object.extend
  firstName: null
  lastName: null

  fullName: (->
    "#{@get 'firstName'} #{@get 'lastName'}"
  ).property('firstName', 'lastName')

App.IndexController = Ember.ObjectController.extend
  greeting: (->
    "Hello, #{@get 'fullName'}!"
  ).property('fullName')

App.IndexRoute = Ember.Route.extend
  model: ->
    App.Person.create firstName: 'World', lastName: ''
