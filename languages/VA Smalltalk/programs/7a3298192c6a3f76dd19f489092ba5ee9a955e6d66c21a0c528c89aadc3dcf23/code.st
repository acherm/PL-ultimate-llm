| rootConfig importConfig |
rootConfig := AbtXmlDeserializationConfiguration newMappingParserConfiguration.
rootConfig mappingSpecName: SstWebServicesParserApp abtXmlCacheKey.
rootConfig handlerClass: SstWsdlSaxHandler.
importConfig := rootConfig newConfiguration.
importConfig handlerClass: SstWsdlImportHandler.
rootConfig useConfiguration: importConfig forElementNamed: 'import'
  inNamespace: SstWebServicesParserApp abtXmlCacheKey.
AbtXmlObjectCache current addDeserializationConfiguration: rootConfig
  named: SstWebServicesParserApp abtXmlCacheKey.
