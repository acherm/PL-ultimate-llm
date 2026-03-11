%% Query persons whose age is above 30
%% Xcerpt rule-based query example

construct {
  result {
    person {
      name { $name },
      age  { $age }
    }
  }
}
where {
  some $doc in "persons.xml" : {
    persons {
      person {
        name { $name },
        age  { $age }
      }
    }
  },
  $age > 30
}
