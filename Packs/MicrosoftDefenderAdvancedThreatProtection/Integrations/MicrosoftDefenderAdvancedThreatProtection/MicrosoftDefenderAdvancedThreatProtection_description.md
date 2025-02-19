Microsoft integrations (Graph and Azure) in Cortex XSOAR use Azure Active Directory applications to authenticate with Microsoft APIs. These integrations use OAuth 2.0 and OpenID Connect standard-compliant authentication services, which use an Application to sign-in or delegate authentication. For more information, see the Microsoft identity platform overview.

There are 2 application authentication methods available:

 * [Cortex XSOAR Application](https://xsoar.pan.dev/docs/reference/articles/microsoft-integrations---authentication#cortex-xsoar-application)
 * [Self-Deployed Application](https://xsoar.pan.dev/docs/reference/articles/microsoft-integrations---authentication#self-deployed-application)

Depending on the authentication method that you use, the integration parameters might change.

To allow us access to Microsoft Defender Advanced Threat Protection, an admin has to approve our app using an admin consent flow, by clicking on the following [link](https://oproxy.demisto.ninja/ms-defender-atp).
After authorizing the Demisto app, you will get an ID, Token, and Key, which should be inserted in the integration instance configuration's corresponding fields.

## Authorize Cortex XSOAR for Azure Active Directory Users (Self deployed Azure App)

There are two different authentication methods for self-deployed configuration: 
- [Client Credentials flow](https://learn.microsoft.com/en-us/microsoft-365/security/defender-endpoint/exposed-apis-create-app-webapp?view=o365-worldwide)
- [Authorization Code flow](https://learn.microsoft.com/en-us/microsoft-365/security/defender-endpoint/exposed-apis-create-app-nativeapp?view=o365-worldwide)
### Authentication Using the Authorization Code Flow
**Note**: When using the Authorization Code Flow, please make sure the user you authenticate with has the required role permissions. See [this](https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/initiate-autoir-investigation?view=o365-worldwide#permissions) as an example.
1. To use a self-configured Azure application, you need to add a new Azure App Registration in the Azure Portal. To add the registration, refer to the following [Microsoft article](https://docs.microsoft.com/en-us/microsoft-365/security/defender/api-create-app-web?view=o365-worldwide#create-an-app) steps 1-8.
2. In the **ID** field, enter your Client/Application ID. 
3. In the **Key** field, enter your Client Secret.
4. In the **Token** field, enter your Tenant ID .
5. In the **Authentication Type** field, select the **Authorization Code** option.
6. Mark **Use a self-deployed Azure Application** as true.
7. In the **Application redirect URI** field, enter your Application redirect URI.
8. In the **Authorization code** field, enter your Authorization code.
9. Save the instance.