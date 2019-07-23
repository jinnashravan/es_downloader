compose {
  name('es_downloader')
  dockerRegistry('226817515299.dkr.ecr.eu-west-1.amazonaws.com', true)
  publishPythonPackage()

  suites {
    suite(name: 'es_downloader', resultXml: "unit_results.xml", publish: false, expose: ["/tmp/unit_results.xml"])
  }
}
