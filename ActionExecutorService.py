{
  "protos": [
    "src/LicenseService.Service/Protos/docusign/license/license_service.proto"
  ],
  "urls": [
    {
      "url": "docusign.license.v1/SayHello",
      "name": "greet-service-sayhello",
      "data": {
        "name": "Test"
      },
      "expectedStatus": 0,
      "expectedBody": {
        "message": "Hello, Test!"
      }
    }
  ]
}
