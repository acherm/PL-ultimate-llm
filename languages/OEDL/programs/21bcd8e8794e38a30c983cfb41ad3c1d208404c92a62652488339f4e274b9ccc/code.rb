defApplication('simple_ping') do |app|
  app.description = 'Simple Definition for the simple_ping application'
  app.binary_path = '/bin/ping'
  app.defProperty('target', 'Address to ping', '', {:type => :string})
  app.defProperty('count', 'Number of times to ping', '-c', {:type => :integer})
end

defGroup('Sender', 'node11') do |g|
  g.addApplication("simple_ping") do |app|
    app.setProperty('target', '8.8.8.8')
    app.setProperty('count', 3)
    app.measure('ping', :samples => 1)
  end
end

onEvent(:ALL_UP_AND_INSTALLED) do |event|
  info "This is my first OMF experiment"
  allGroups.startApplications
  after 15 do
    allGroups.stopApplications
  end
  after 10 do
    Experiment.done
  end
end
