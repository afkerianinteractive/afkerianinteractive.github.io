#!/usr/bin/env python3
"""Rewrite first-party legal TXT content without changing public paths.

This is an owner-invoked content migration for the three game products and the
public website. Authentic upstream license files are intentionally excluded.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE_EN = "July 22, 2026"
DATE_ES = "22 de julio de 2026"
CONTACT = "afkerian.support@gmail.com"

PRODUCTS = {
    "xo-arcade": {
        "name": "XO Arcade: Infinity Edition",
        "ads_en": "anchored banner advertisements and occasional interstitial advertisements",
        "ads_es": "anuncios de banner anclado y anuncios intersticiales ocasionales",
        "reward_en": "",
        "reward_es": "",
        "backup_en": (
            "Android backup or device-transfer services may copy supported local data "
            "when enabled by Android, the device manufacturer, or the user."
        ),
        "backup_es": (
            "Los servicios de copia o transferencia de Android pueden copiar datos "
            "locales compatibles cuando Android, el fabricante o el usuario los habilitan."
        ),
        "network_en": "",
        "network_es": "",
        "creative_en": (
            "The Game includes Kenney sound assets made available under CC0 1.0 and "
            "audio generated using ElevenLabs and Suno. Separate notices identify the "
            "sources and governing terms."
        ),
        "creative_es": (
            "El Juego incluye sonidos de Kenney ofrecidos bajo CC0 1.0 y audio generado "
            "mediante ElevenLabs y Suno. Avisos separados identifican las fuentes y los "
            "términos aplicables."
        ),
        "inventory_en": [
            "Google AdMob and Google User Messaging Platform",
            "ElevenLabs-generated voice and sound effects",
            "Kenney Casino Audio and UI Audio assets under CC0 1.0",
            "Suno-generated music",
        ],
        "inventory_es": [
            "Google AdMob y Google User Messaging Platform",
            "voces y efectos generados mediante ElevenLabs",
            "recursos Casino Audio y UI Audio de Kenney bajo CC0 1.0",
            "música generada mediante Suno",
        ],
    },
    "air-strike-arcade": {
        "name": "Air Strike Arcade",
        "ads_en": "anchored banner advertisements and occasional interstitial advertisements",
        "ads_es": "anuncios de banner anclado y anuncios intersticiales ocasionales",
        "reward_en": "",
        "reward_es": "",
        "backup_en": (
            "Android backup or device-transfer services may copy supported local data "
            "when enabled by Android, the device manufacturer, or the user."
        ),
        "backup_es": (
            "Los servicios de copia o transferencia de Android pueden copiar datos "
            "locales compatibles cuando Android, el fabricante o el usuario los habilitan."
        ),
        "network_en": "",
        "network_es": "",
        "creative_en": (
            "The Game includes sound effects sourced from Pixabay and music generated "
            "using Suno. Separate notices identify the sources and governing terms."
        ),
        "creative_es": (
            "El Juego incluye efectos de sonido obtenidos de Pixabay y música generada "
            "mediante Suno. Avisos separados identifican las fuentes y los términos aplicables."
        ),
        "inventory_en": [
            "Google AdMob and Google User Messaging Platform",
            "Pixabay sound effects",
            "Suno-generated music",
        ],
        "inventory_es": [
            "Google AdMob y Google User Messaging Platform",
            "efectos de sonido de Pixabay",
            "música generada mediante Suno",
        ],
    },
    "tap-odyssey": {
        "name": "Tap Odyssey",
        "ads_en": "anchored banner advertisements and occasional interstitial advertisements",
        "ads_es": "anuncios de banner anclado y anuncios intersticiales ocasionales",
        "reward_en": (
            " The Game also offers an optional rewarded advertisement. A completed "
            "rewarded advertisement grants the in-Game benefit described at the point of offer."
        ),
        "reward_es": (
            " El Juego también ofrece un anuncio recompensado opcional. Completarlo "
            "concede el beneficio descrito dentro del Juego al momento de la oferta."
        ),
        "backup_en": (
            "The Game permits Android backup and device transfer for supported preferences, "
            "database content, and DataStore content. Android, the device manufacturer, and "
            "the user's settings control whether a backup or transfer occurs."
        ),
        "backup_es": (
            "El Juego permite copia y transferencia de Android para preferencias, contenido "
            "de base de datos y contenido de DataStore compatibles. Android, el fabricante "
            "y los ajustes del usuario controlan si la copia o transferencia ocurre."
        ),
        "network_en": (
            "The Game may send a short Network Time Protocol request to time.google.com "
            "to verify time-dependent game rules. The time service necessarily receives "
            "network information such as the requesting IP address and returns time data; "
            "the Game treats failure or timeout as an unavailable verification result."
        ),
        "network_es": (
            "El Juego puede enviar una solicitud breve del Protocolo de Tiempo de Red a "
            "time.google.com para verificar reglas que dependen del tiempo. El servicio "
            "recibe necesariamente información de red, como la dirección IP solicitante, "
            "y devuelve datos horarios; el Juego trata un fallo o tiempo de espera como "
            "un resultado de verificación no disponible."
        ),
        "creative_en": (
            "The Game includes visual assets generated using OpenAI services, sound effects "
            "sourced from Pixabay, and music generated using Suno. Separate notices identify "
            "the sources and governing terms."
        ),
        "creative_es": (
            "El Juego incluye recursos visuales generados mediante servicios de OpenAI, "
            "efectos de sonido obtenidos de Pixabay y música generada mediante Suno. Avisos "
            "separados identifican las fuentes y los términos aplicables."
        ),
        "inventory_en": [
            "Google AdMob and Google User Messaging Platform",
            "OpenAI / ChatGPT-generated visual assets",
            "Pixabay sound effects",
            "Suno-generated music",
        ],
        "inventory_es": [
            "Google AdMob y Google User Messaging Platform",
            "recursos visuales generados mediante OpenAI / ChatGPT",
            "efectos de sonido de Pixabay",
            "música generada mediante Suno",
        ],
    },
}


def header(title: str, product: str, language: str) -> str:
    if language == "es-419":
        dates = (
            f"Fecha efectiva: {DATE_ES}\n"
            f"Última actualización: {DATE_ES}"
        )
    else:
        dates = (
            f"Effective Date: {DATE_EN}\n"
            f"Last Updated: {DATE_EN}"
        )
    return f"{title}\n{product}\n\n{dates}\n\n"


def privacy_en(product: dict[str, object]) -> str:
    name = str(product["name"])
    network = (
        "\n\n" + str(product["network_en"])
        if product["network_en"]
        else ""
    )
    return header("PRIVACY POLICY", name, "en-US") + f"""1. SCOPE AND IDENTITY

This Privacy Policy explains how I, Jesus Afkerian, process information in connection with {name} (the “Game”). In this Policy, “I,” “me,” and “my” refer only to Jesus Afkerian. I am the individual who publishes and operates the Game. This Policy covers the Game and support communications about it. Google Play, Google services, and other third-party services operate under their own policies.

The Game does not require a first-party account or ask you to enter a civil name, postal address, contacts, or payment information during ordinary play. If you contact support, I receive the email address, message, attachments, and other information you choose to send.

2. AUDIENCE AND PERMITTED TERRITORY

The Game is intended only for adults and is not directed to children. It does not independently verify age. You must be at least 18 and have reached the age of majority and contractual capacity where you live, whichever standard is higher.

The permitted distribution territory is stated at:
https://afkerianinteractive.github.io/legal/PERMITTED_TERRITORY.txt

3. LOCAL GAME DATA AND ANDROID BACKUP

Progress, scores, preferences, and ordinary game state are stored primarily on the device. I do not operate a first-party gameplay-profile server that receives this local state.

{product["backup_en"]}

Uninstalling the Game, clearing its data, device loss, corruption, or backup and restore behavior can delete, retain, copy, or restore local information. Recovery is not guaranteed.

4. NETWORK SERVICES

The Game is not completely offline. It connects to services used for advertising, privacy messaging, analytics, crash reporting, installation and session measurement, security, and fraud prevention. These services include Google Mobile Ads, Google User Messaging Platform (“UMP”), Google Analytics for Firebase, Firebase Crashlytics, Firebase Installations, and Firebase Sessions.{network}

5. ADVERTISING AND PRIVACY MESSAGING

The Game is currently offered without a purchase price and is supported by advertising. Jesus Afkerian may receive advertising revenue through Google AdMob. Advertising revenue is not an amount paid by the user.

The Game uses {product["ads_en"]}.{product["reward_en"]} It does not use App Open or native advertisements.

UMP determines whether the advertising code may request ads and may present a regional consent message or Privacy Options entry. UMP gates advertising only. A UMP choice does not disable Analytics, Crashlytics, Firebase Installations, Firebase Sessions{", the network-time request described above" if product["network_en"] else ""}, or all network activity.

An advertising failure does not block ordinary navigation or erase local progress. A choice against personalized advertising may still allow contextual or limited ads and processing for measurement, security, frequency control, diagnostics, and fraud prevention.

6. AUTOMATIC PROCESSING BY GOOGLE MOBILE ADS

Google states that the Google Mobile Ads SDK automatically processes and shares IP address information that may be used to estimate approximate location, Game and advertising interactions, diagnostic information, and device or account identifiers for advertising, analytics, and fraud prevention. Supported identifiers may include the Android Advertising ID and app set identifiers. Google states that this data is encrypted in transit.

7. ANALYTICS, CRASHLYTICS, INSTALLATIONS, AND SESSIONS

Google Analytics for Firebase automatically collects default app, device, session, screen, and interaction information; an app-instance identifier; approximate location derived from IP address; and the Advertising ID when available and not disabled. The Game does not send first-party authored custom Analytics events, User-ID values, or custom user properties.

Firebase Crashlytics processes crash stack traces, relevant application state, device metadata, and a Crashlytics installation identifier when crash reporting operates. Crashlytics operates in public release versions of the Game, and the Game does not add custom Crashlytics logs, keys, user IDs, or user-content reports.

Firebase Installations creates a per-installation identifier. Firebase Sessions processes session, app, device, network-connection, and performance metadata. Analytics breadcrumbs may be associated with crash reports through Google SDK integration.

8. DATA CATEGORIES

Category: Approximate location
Source: IP address processed by Google Mobile Ads and Google Analytics for Firebase.
Purpose: Advertising, analytics, security, and fraud prevention.
Recipients: Google and service providers acting for the relevant Google services.
Retention criterion: Provider settings, service purpose, security and fraud-prevention needs, legal obligations, and valid deletion requests.

Category: Game and advertising interactions
Source: The Game, Google Mobile Ads, and Google Analytics for Firebase.
Purpose: Advertising delivery, measurement, analytics, frequency control, security, and fraud prevention.
Recipients: Google and service providers acting for the relevant Google services.
Retention criterion: Provider settings, measurement periods, security and fraud-prevention needs, legal obligations, and valid deletion requests.

Category: Crash logs and diagnostics
Source: Google Mobile Ads, Firebase Crashlytics, Firebase Sessions, the device, and the Game.
Purpose: Stability, debugging, performance, analytics, security, and fraud prevention.
Recipients: Google and service providers acting for the relevant Google services.
Retention criterion: Time needed to diagnose and aggregate failures, provider settings, security needs, legal obligations, and valid deletion requests.

Category: Device and other identifiers
Source: Google Mobile Ads, Google Analytics for Firebase, Firebase Crashlytics, and Firebase Installations.
Purpose: Advertising, analytics, installation and session measurement, crash management, security, and fraud prevention.
Recipients: Google and service providers acting for the relevant Google services.
Retention criterion: Provider settings, service continuity, security and fraud-prevention needs, legal obligations, and valid deletion requests.

Category: Support communications
Source: Information you choose to send by email.
Purpose: Responding to the request, maintaining support records, protecting rights, and preventing abuse.
Recipients: Jesus Afkerian and email or infrastructure providers needed to handle the request.
Retention criterion: Time reasonably necessary to handle the request, maintain appropriate records, resolve disputes, protect the service, and meet legal obligations.

9. REQUIRED, OPTIONAL, AND EPHEMERAL PROCESSING

You are not required to contact me or create a first-party account to play. Automatic SDK processing is not described as ephemeral because advertising, analytics, installation, fraud-prevention, diagnostic, and crash records may persist after an individual network request. UMP, Google controls, and Android advertising settings have different scopes; the Game does not provide one control that disables every service listed in this Policy.

10. PROVIDERS AND INTERNATIONAL PROCESSING

Google LLC and its affiliates provide AdMob, UMP, Analytics, Crashlytics, Installations, and Sessions. Google may process information in the United States and other countries where it or its processors operate. Google determines its own infrastructure, personnel, subprocessors, retention settings, and legal bases under its terms and policies.

Google Privacy Policy:
https://policies.google.com/privacy

Google service disclosures:
https://developers.google.com/admob/android/privacy/play-data-disclosure
https://firebase.google.com/docs/android/play-data-disclosure

11. RETENTION AND DELETION

Local Game data remains subject to device storage, Android backup or transfer, user deletion, and uninstall behavior. Support information is retained under the criterion stated in Section 8. Google controls retention for data it processes in its services, subject to provider settings and applicable terms. I may retain information when reasonably necessary for security, fraud prevention, dispute resolution, enforcement, or legal obligations.

12. PRIVACY RIGHTS AND CHOICES

Depending on your residence, the law that applies to the processing, and any statutory thresholds or exceptions, you may have rights to request access, correction, deletion, or a copy of personal information, or to object to or limit certain processing. You may send a request to {CONTACT}. I may need information reasonably necessary to verify and respond to the request. You may also use UMP Privacy Options when shown, Android advertising controls, Google account controls, and provider deletion tools.

I do not exchange personal information for money. Some laws may characterize advertising-related disclosure as a sale, sharing, or targeted advertising even without a monetary payment. Whether a particular law or right applies depends on the relevant facts and legal requirements.

13. CHILDREN

The Game is not intended for children or for anyone who lacks legal capacity to use it. If you believe a child sent personal information through support, contact me so I can evaluate and address the request.

14. SECURITY

I use reasonable administrative and technical measures appropriate to the information I control. No storage or transmission method is completely secure, and I cannot guarantee absolute security.

15. LEGAL DISCLOSURES

Information may be preserved or disclosed when reasonably necessary to comply with valid legal process, protect users or the public, investigate abuse or security incidents, enforce applicable terms, or establish, exercise, or defend legal claims.

16. CHANGES

I may update this Policy when the Game, service providers, or applicable requirements change. The updated document will state its effective date. Material changes will receive reasonably conspicuous notice where appropriate.

17. CONTACT

Jesus Afkerian
{CONTACT}
"""


def privacy_es(product: dict[str, object]) -> str:
    name = str(product["name"])
    network = (
        "\n\n" + str(product["network_es"])
        if product["network_es"]
        else ""
    )
    return header("POLÍTICA DE PRIVACIDAD", name, "es-419") + f"""1. ALCANCE E IDENTIDAD

Esta Política de Privacidad explica cómo yo, Jesus Afkerian, trato información en relación con {name} (el «Juego»). En esta Política, «yo» y «mi» se refieren únicamente a Jesus Afkerian. Soy la persona física que publica y opera el Juego. Esta Política cubre el Juego y las comunicaciones de soporte relacionadas. Google Play, los servicios de Google y otros servicios de terceros operan bajo sus propias políticas.

El Juego no exige una cuenta propia ni solicita nombre civil, dirección postal, contactos o información de pago durante el uso ordinario. Si contactas soporte, recibo la dirección de correo, mensaje, adjuntos y demás información que decidas enviar.

2. PÚBLICO Y TERRITORIO PERMITIDO

El Juego está destinado exclusivamente a adultos y no se dirige a niños. No verifica la edad de forma independiente. Debes tener al menos 18 años y haber alcanzado la mayoría de edad y capacidad contractual del lugar donde vives, aplicándose el estándar más alto.

El territorio de distribución permitido se indica en:
https://afkerianinteractive.github.io/legal/PERMITTED_TERRITORY_ES.txt

3. DATOS LOCALES Y COPIA DE ANDROID

El progreso, puntuaciones, preferencias y estado ordinario se almacenan principalmente en el dispositivo. No opero un servidor propio de perfiles de juego que reciba ese estado local.

{product["backup_es"]}

Desinstalar el Juego, borrar sus datos, perder el dispositivo, la corrupción o el funcionamiento de copia y restauración pueden eliminar, conservar, copiar o restaurar información local. No se garantiza recuperación.

4. SERVICIOS DE RED

El Juego no es totalmente offline. Se conecta a servicios de publicidad, mensajes de privacidad, análisis, informes de fallos, medición de instalaciones y sesiones, seguridad y prevención del fraude. Estos servicios incluyen Google Mobile Ads, Google User Messaging Platform («UMP»), Google Analytics for Firebase, Firebase Crashlytics, Firebase Installations y Firebase Sessions.{network}

5. PUBLICIDAD Y MENSAJES DE PRIVACIDAD

El Juego se ofrece actualmente sin precio de compra y se financia mediante publicidad. Jesus Afkerian puede recibir ingresos publicitarios a través de Google AdMob. Los ingresos publicitarios no son una cantidad pagada por el usuario.

El Juego usa {product["ads_es"]}.{product["reward_es"]} No usa anuncios App Open ni nativos.

UMP determina si el código publicitario puede solicitar anuncios y puede presentar un mensaje regional de consentimiento u Opciones de privacidad. UMP solo controla publicidad. Una elección de UMP no desactiva Analytics, Crashlytics, Firebase Installations, Firebase Sessions{", la solicitud de hora de red descrita anteriormente" if product["network_es"] else ""} ni toda actividad de red.

Un fallo publicitario no bloquea la navegación ordinaria ni borra progreso local. Rechazar publicidad personalizada todavía puede permitir anuncios contextuales o limitados y tratamiento para medición, seguridad, frecuencia, diagnóstico y prevención del fraude.

6. TRATAMIENTO AUTOMÁTICO DE GOOGLE MOBILE ADS

Google indica que Google Mobile Ads trata y comparte automáticamente la dirección IP, que puede estimar ubicación aproximada; interacciones con el Juego y la publicidad; diagnósticos; e identificadores de dispositivo o cuenta para publicidad, análisis y prevención del fraude. Los identificadores compatibles pueden incluir el ID de publicidad de Android y los identificadores de conjunto de apps. Google indica que estos datos se cifran en tránsito.

7. ANALYTICS, CRASHLYTICS, INSTALLATIONS Y SESSIONS

Google Analytics for Firebase recopila automáticamente información predeterminada del Juego, dispositivo, sesión, pantallas e interacciones; un identificador de instancia; ubicación aproximada derivada de IP; e ID de publicidad cuando está disponible y no desactivado. El Juego no envía eventos personalizados de Analytics escritos por el propietario, valores User-ID ni propiedades personalizadas.

Firebase Crashlytics trata trazas de fallos, estado relevante, metadatos del dispositivo y un identificador de instalación cuando opera el informe de fallos. El Juego habilita Crashlytics en compilaciones release y no añade registros, claves, identificadores de usuario ni informes de contenido del usuario personalizados.

Firebase Installations crea un identificador por instalación. Firebase Sessions trata metadatos de sesión, Juego, dispositivo, conexión y rendimiento. La integración de Google puede asociar eventos anteriores de Analytics con informes de fallos.

8. CATEGORÍAS DE DATOS

Categoría: Ubicación aproximada
Fuente: Dirección IP tratada por Google Mobile Ads y Google Analytics for Firebase.
Finalidad: Publicidad, análisis, seguridad y prevención del fraude.
Destinatarios: Google y proveedores que actúan para los servicios pertinentes de Google.
Criterio de conservación: Ajustes del proveedor, finalidad del servicio, seguridad, fraude, obligaciones legales y solicitudes válidas de eliminación.

Categoría: Interacciones con el Juego y la publicidad
Fuente: El Juego, Google Mobile Ads y Google Analytics for Firebase.
Finalidad: Entrega publicitaria, medición, análisis, control de frecuencia, seguridad y prevención del fraude.
Destinatarios: Google y proveedores que actúan para los servicios pertinentes de Google.
Criterio de conservación: Ajustes del proveedor, períodos de medición, seguridad, fraude, obligaciones legales y solicitudes válidas de eliminación.

Categoría: Registros de fallos y diagnósticos
Fuente: Google Mobile Ads, Firebase Crashlytics, Firebase Sessions, el dispositivo y el Juego.
Finalidad: Estabilidad, depuración, rendimiento, análisis, seguridad y prevención del fraude.
Destinatarios: Google y proveedores que actúan para los servicios pertinentes de Google.
Criterio de conservación: Tiempo para diagnosticar y agregar fallos, ajustes del proveedor, seguridad, obligaciones legales y solicitudes válidas de eliminación.

Categoría: Identificadores de dispositivo y otros
Fuente: Google Mobile Ads, Google Analytics for Firebase, Firebase Crashlytics y Firebase Installations.
Finalidad: Publicidad, análisis, medición de instalaciones y sesiones, gestión de fallos, seguridad y prevención del fraude.
Destinatarios: Google y proveedores que actúan para los servicios pertinentes de Google.
Criterio de conservación: Ajustes del proveedor, continuidad del servicio, seguridad, fraude, obligaciones legales y solicitudes válidas de eliminación.

Categoría: Comunicaciones de soporte
Fuente: Información que decides enviar por correo.
Finalidad: Responder la solicitud, mantener registros de soporte, proteger derechos y prevenir abuso.
Destinatarios: Jesus Afkerian y proveedores de correo o infraestructura necesarios para gestionar la solicitud.
Criterio de conservación: Tiempo razonablemente necesario para gestionar la solicitud, mantener registros apropiados, resolver disputas, proteger el servicio y cumplir obligaciones legales.

9. CARÁCTER OBLIGATORIO, OPCIONAL Y EFÍMERO

No necesitas contactarme ni crear una cuenta propia para jugar. El tratamiento automático de SDK no se describe como efímero porque los registros publicitarios, analíticos, de instalación, fraude, diagnóstico y fallos pueden persistir después de una solicitud de red. UMP, los controles de Google y los ajustes publicitarios de Android tienen alcances diferentes; el Juego no ofrece un único control que desactive todos los servicios enumerados.

10. PROVEEDORES Y TRATAMIENTO INTERNACIONAL

Google LLC y sus afiliadas proporcionan AdMob, UMP, Analytics, Crashlytics, Installations y Sessions. Google puede tratar información en Estados Unidos y otros países donde opera o donde operan sus encargados. Google determina su infraestructura, personal, subencargados, ajustes de conservación y bases jurídicas bajo sus términos y políticas.

Política de Privacidad de Google:
https://policies.google.com/privacy

Divulgaciones de servicios de Google:
https://developers.google.com/admob/android/privacy/play-data-disclosure
https://firebase.google.com/docs/android/play-data-disclosure

11. CONSERVACIÓN Y ELIMINACIÓN

Los datos locales quedan sujetos al almacenamiento del dispositivo, copia o transferencia de Android, eliminación por el usuario y desinstalación. La información de soporte se conserva según el criterio de la Sección 8. Google controla la conservación de datos en sus servicios, sujeto a ajustes y términos aplicables. Puedo conservar información cuando sea razonablemente necesario para seguridad, fraude, disputas, ejecución u obligaciones legales.

12. DERECHOS Y OPCIONES DE PRIVACIDAD

Según tu residencia, la ley aplicable al tratamiento y los umbrales o excepciones legales, puedes tener derechos para solicitar acceso, corrección, eliminación o copia, u oponerte o limitar cierto tratamiento. Puedes enviar una solicitud a {CONTACT}. Puedo necesitar información razonablemente necesaria para verificar y responder. También puedes usar Opciones de privacidad de UMP cuando aparezcan, controles publicitarios de Android, controles de cuenta de Google y herramientas de eliminación del proveedor.

No intercambio información personal por dinero. Algunas leyes pueden calificar una divulgación publicitaria como venta, intercambio o publicidad dirigida aun sin pago monetario. La aplicación de una ley o derecho depende de los hechos y requisitos pertinentes.

13. NIÑOS

El Juego no está destinado a niños ni a personas sin capacidad legal para usarlo. Si crees que un niño envió información mediante soporte, contáctame para que pueda evaluar y atender la solicitud.

14. SEGURIDAD

Uso medidas administrativas y técnicas razonables apropiadas para la información bajo mi control. Ningún método de almacenamiento o transmisión es completamente seguro y no puedo garantizar seguridad absoluta.

15. DIVULGACIONES LEGALES

La información puede conservarse o divulgarse cuando sea razonablemente necesario para cumplir proceso legal válido, proteger usuarios o al público, investigar abuso o incidentes, ejecutar términos aplicables o establecer, ejercer o defender reclamaciones.

16. CAMBIOS

Puedo actualizar esta Política cuando cambien el Juego, los proveedores o los requisitos aplicables. El documento actualizado indicará su fecha efectiva. Los cambios materiales recibirán aviso razonablemente visible cuando corresponda.

17. CONTACTO

Jesus Afkerian
{CONTACT}
"""


def terms_en(product: dict[str, object]) -> str:
    name = str(product["name"])
    return header("TERMS OF SERVICE", name, "en-US") + f"""1. AGREEMENT AND OPERATOR

These Terms of Service are an agreement between you and Jesus Afkerian, an individual who publishes and operates the Game. These Terms govern {name} (the “Game”).

If you do not agree, do not download, install, access, or use the Game. If it is installed, stop using it and uninstall it.

2. ADULT ELIGIBILITY

You may use the Game only if you are at least 18 and have reached the age of majority and contractual capacity where you live, whichever standard is higher. The Game is not directed to children.

3. PERMITTED TERRITORY

Use is authorized only in the territory identified at:
https://afkerianinteractive.github.io/legal/PERMITTED_TERRITORY.txt

Access to the Game or these Terms from another location does not grant authorization there. You are responsible for complying with mandatory local law.

4. LIMITED LICENSE

Subject to these Terms, Jesus Afkerian grants you a personal, limited, revocable, nonexclusive, nontransferable, and nonsublicensable license to install and use the Game on a compatible device for personal, noncommercial entertainment in the permitted territory.

No ownership interest is transferred. Except where applicable law does not permit restriction, you may not copy, sell, rent, sublicense, distribute, publicly perform, make available, reverse engineer, circumvent technical protections, extract assets, or create derivative works from the Game.

5. GAME FUNCTION, LOCAL DATA, AND BACKUP

The Game stores progress, scores, preferences, and ordinary state primarily on the device. {product["backup_en"]} Uninstalling, clearing data, device loss, corruption, or backup behavior may delete, retain, copy, or restore data. Jesus Afkerian does not promise recovery, uninterrupted availability, or compatibility with every device.

6. ADVERTISING

The Game is currently offered without a purchase price and is supported by advertising. Jesus Afkerian may receive advertising revenue through Google AdMob. Advertising revenue is not an amount paid by the user.

The Game uses {product["ads_en"]}.{product["reward_en"]} It does not use App Open or native advertisements. UMP gates advertising requests only; it does not disable analytics, crash reporting, installation or session measurement, security services, or all network activity. Advertising failure must not be treated as permission to bypass technical controls.

7. PRIVACY

The Privacy Policy explains local data, advertising, Analytics, Crashlytics, Installations, Sessions, support communications, and available choices:
https://afkerianinteractive.github.io/{next(key for key, value in PRODUCTS.items() if value is product)}/privacy-policy.html

The Game is not completely offline.

8. ACCEPTABLE USE

You may not misuse the Game, interfere with its operation, exploit defects, automate interactions in a manner that harms the service, evade advertising or eligibility controls, introduce malicious code, violate another person's rights, or use the Game for unlawful activity.

9. OWNERSHIP AND THIRD-PARTY MATERIALS

Jesus Afkerian and his licensors retain their respective rights in the Game, including code, design, text, graphics, audio, and other content. {product["creative_en"]}

Third-party names and marks belong to their owners. No license to a third-party mark is granted except as necessary to identify the relevant source.

10. UPDATES AND AVAILABILITY

The Game may be corrected, updated, changed, suspended, or discontinued. Features may vary by device, operating-system version, region, network, provider availability, and configuration. To the extent permitted by law, no particular feature or period of availability is promised.

11. THIRD-PARTY SERVICES

Google Play, Google AdMob, UMP, Firebase services, and creative or asset providers are third parties with their own terms and policies. Jesus Afkerian does not control their infrastructure, availability, security, or independent processing.

12. EXPORT CONTROLS AND SANCTIONS

You may not use, export, reexport, or transfer the Game in violation of applicable export-control, sanctions, or trade laws. You represent that you are not prohibited from receiving the Game under laws that apply to you.

13. SUPPORT AND FEEDBACK

Support is offered at {CONTACT} without a guaranteed response time or outcome.

To the extent you voluntarily provide feedback, you grant Jesus Afkerian a nonexclusive, worldwide, perpetual, irrevocable, royalty-free, transferable and sublicensable license to use it for lawful product and business purposes. This license does not cover personal information, confidential information, or third-party material you lack authority to license.

14. SUSPENSION AND TERMINATION

Your license ends automatically if you materially breach these Terms. You may end it at any time by stopping use and uninstalling the Game. Provisions that by their nature should survive, including ownership, disclaimers, liability limits, indemnity, governing law, and general terms, continue to the extent permitted by law.

15. DISCLAIMERS

TO THE MAXIMUM EXTENT PERMITTED BY LAW, THE GAME IS PROVIDED “AS IS” AND “AS AVAILABLE,” WITH ALL FAULTS. JESUS AFKERIAN DISCLAIMS IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, NON-INFRINGEMENT, QUIET ENJOYMENT, AND WARRANTIES ARISING FROM COURSE OF DEALING OR USAGE OF TRADE.

Nothing in these Terms excludes a warranty or remedy that cannot lawfully be excluded.

16. LIMITATION OF LIABILITY

TO THE MAXIMUM EXTENT PERMITTED BY LAW, JESUS AFKERIAN WILL NOT BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES, OR FOR LOSS OF DATA, PROFITS, REVENUE, GOODWILL, OR BUSINESS INTERRUPTION, ARISING FROM OR RELATED TO THE GAME.

TO THE MAXIMUM EXTENT PERMITTED BY LAW, JESUS AFKERIAN'S AGGREGATE LIABILITY ARISING FROM OR RELATED TO THE GAME WILL NOT EXCEED THE GREATER OF THE AMOUNT YOU PAID DIRECTLY TO JESUS AFKERIAN FOR THE GAME DURING THE TWELVE MONTHS BEFORE THE EVENT GIVING RISE TO THE CLAIM OR TEN U.S. DOLLARS. THIS LIMIT DOES NOT APPLY WHERE APPLICABLE LAW REQUIRES A DIFFERENT RESULT.

17. NARROW INDEMNITY

To the maximum extent permitted by law, you will defend, indemnify, and hold Jesus Afkerian harmless from third-party claims, damages, judgments, losses, and reasonable costs arising from your unlawful use of the Game, your material breach of these Terms, or content you submit through support that infringes another person's rights.

Jesus Afkerian will give reasonably prompt notice and permit you to control the defense with counsel reasonably acceptable to him. You may not settle a claim without Jesus Afkerian's prior written consent if the settlement admits fault by him, imposes a nonmonetary obligation on him, or does not fully release him; consent will not be unreasonably withheld. Jesus Afkerian may participate with counsel at his own expense.

18. MANDATORY RIGHTS

These Terms do not waive consumer protections, statutory rights, remedies, or jurisdictional rules that cannot lawfully be waived or limited.

19. GOVERNING LAW AND VENUE

These Terms are governed by Florida law, without regard to conflict-of-laws principles, except where mandatory law requires otherwise. Subject to any nonwaivable right to another forum, proceedings must be brought in the state courts located in Orange County, Florida, or the federal courts serving Orange County, Florida.

20. CHANGES

Jesus Afkerian may update these Terms for changes to the Game, providers, risk, or applicable requirements. Updated Terms will state their effective date and material changes will receive reasonably conspicuous notice where appropriate.

Publication alone, silence, inaction, or keeping the Game installed does not constitute acceptance of updated Terms. Continued access or use after reasonably conspicuous notice and the stated effective date is the conduct relied upon as assent, to the maximum extent permitted by law.

21. GENERAL

These Terms, the Privacy Policy, and incorporated notices form the agreement concerning the Game. If a provision is unenforceable, it will be enforced to the maximum lawful extent and the remainder will continue. Failure to enforce a provision is not a waiver. You may not assign these Terms without prior written consent; Jesus Afkerian may assign them in connection with a lawful transfer of the Game or his business interests, subject to applicable law.

22. CONTACT

Jesus Afkerian
{CONTACT}
"""


def terms_es(product: dict[str, object]) -> str:
    name = str(product["name"])
    slug = next(key for key, value in PRODUCTS.items() if value is product)
    return header("TÉRMINOS DEL SERVICIO", name, "es-419") + f"""1. ACUERDO Y OPERADOR

Estos Términos del Servicio son un acuerdo entre tú y Jesus Afkerian, persona física que publica y opera el Juego. Estos Términos rigen {name} (el «Juego»).

Si no estás de acuerdo, no descargues, instales, accedas ni uses el Juego. Si está instalado, deja de usarlo y desinstálalo.

2. ELEGIBILIDAD ADULTA

Solo puedes usar el Juego si tienes al menos 18 años y alcanzaste la mayoría de edad y capacidad contractual del lugar donde vives, aplicándose el estándar más alto. El Juego no se dirige a niños.

3. TERRITORIO PERMITIDO

El uso solo está autorizado en el territorio identificado en:
https://afkerianinteractive.github.io/legal/PERMITTED_TERRITORY_ES.txt

Acceder al Juego o a estos Términos desde otro lugar no concede autorización allí. Eres responsable de cumplir la ley local obligatoria.

4. LICENCIA LIMITADA

Sujeto a estos Términos, Jesus Afkerian te concede una licencia personal, limitada, revocable, no exclusiva, intransferible y no sublicenciable para instalar y usar el Juego en un dispositivo compatible, para entretenimiento personal y no comercial dentro del territorio permitido.

No se transfiere propiedad. Salvo cuando la ley no permita la restricción, no puedes copiar, vender, alquilar, sublicenciar, distribuir, ejecutar públicamente, poner a disposición, aplicar ingeniería inversa, eludir protecciones, extraer recursos ni crear obras derivadas del Juego.

5. FUNCIÓN, DATOS LOCALES Y COPIA

El Juego almacena progreso, puntuaciones, preferencias y estado ordinario principalmente en el dispositivo. {product["backup_es"]} Desinstalar, borrar datos, perder el dispositivo, la corrupción o las copias pueden eliminar, conservar, copiar o restaurar datos. Jesus Afkerian no promete recuperación, disponibilidad ininterrumpida ni compatibilidad con todo dispositivo.

6. PUBLICIDAD

El Juego se ofrece actualmente sin precio de compra y se financia mediante publicidad. Jesus Afkerian puede recibir ingresos publicitarios a través de Google AdMob. Los ingresos publicitarios no son una cantidad pagada por el usuario.

El Juego usa {product["ads_es"]}.{product["reward_es"]} No usa anuncios App Open ni nativos. UMP solo controla solicitudes publicitarias; no desactiva análisis, informes de fallos, medición de instalaciones o sesiones, seguridad ni toda actividad de red. Un fallo publicitario no concede permiso para eludir controles técnicos.

7. PRIVACIDAD

La Política de Privacidad explica datos locales, publicidad, Analytics, Crashlytics, Installations, Sessions, soporte y opciones:
https://afkerianinteractive.github.io/{slug}/privacy-policy-es.html

El Juego no es totalmente offline.

8. USO ACEPTABLE

No puedes usar indebidamente el Juego, interferir con su funcionamiento, explotar defectos, automatizar interacciones de forma perjudicial, eludir publicidad o elegibilidad, introducir código malicioso, vulnerar derechos ajenos ni usar el Juego para actividades ilícitas.

9. PROPIEDAD Y MATERIAL DE TERCEROS

Jesus Afkerian y sus licenciantes conservan sus respectivos derechos sobre el Juego, incluido código, diseño, texto, gráficos, audio y demás contenido. {product["creative_es"]}

Los nombres y marcas de terceros pertenecen a sus titulares. No se concede licencia sobre una marca de tercero salvo lo necesario para identificar la fuente pertinente.

10. ACTUALIZACIONES Y DISPONIBILIDAD

El Juego puede corregirse, actualizarse, cambiarse, suspenderse o discontinuarse. Las funciones pueden variar por dispositivo, versión del sistema, región, red, disponibilidad del proveedor y configuración. En la medida permitida, no se promete una función o período particular.

11. SERVICIOS DE TERCEROS

Google Play, Google AdMob, UMP, los servicios Firebase y los proveedores creativos o de recursos son terceros con términos y políticas propios. Jesus Afkerian no controla su infraestructura, disponibilidad, seguridad ni tratamiento independiente.

12. EXPORTACIONES Y SANCIONES

No puedes usar, exportar, reexportar ni transferir el Juego infringiendo leyes aplicables de exportación, sanciones o comercio. Declaras que ninguna ley aplicable te prohíbe recibirlo.

13. SOPORTE Y COMENTARIOS

El soporte se ofrece en {CONTACT} sin plazo u resultado garantizado.

En la medida en que proporciones comentarios voluntariamente, otorgas a Jesus Afkerian una licencia no exclusiva, mundial, perpetua, irrevocable, libre de regalías, transferible y sublicenciable para usarlos con fines lícitos de producto y negocio. Esta licencia no cubre información personal, información confidencial ni material de terceros que no estés autorizado a licenciar.

14. SUSPENSIÓN Y TERMINACIÓN

Tu licencia termina automáticamente si incumples materialmente estos Términos. Puedes terminarla dejando de usar y desinstalando el Juego. Las disposiciones que por su naturaleza deban sobrevivir, incluidas propiedad, exclusiones, límites, indemnización, ley aplicable y términos generales, continúan en la medida permitida.

15. EXCLUSIONES DE GARANTÍAS

EN LA MÁXIMA MEDIDA PERMITIDA, EL JUEGO SE OFRECE «TAL CUAL» Y «SEGÚN DISPONIBILIDAD», CON TODOS SUS DEFECTOS. JESUS AFKERIAN EXCLUYE GARANTÍAS IMPLÍCITAS DE COMERCIABILIDAD, IDONEIDAD PARA UN FIN, TÍTULO, NO INFRACCIÓN, DISFRUTE PACÍFICO Y LAS DERIVADAS DEL CURSO DE NEGOCIACIÓN O USO COMERCIAL.

Nada excluye una garantía o remedio que legalmente no pueda excluirse.

16. LIMITACIÓN DE RESPONSABILIDAD

EN LA MÁXIMA MEDIDA PERMITIDA, JESUS AFKERIAN NO RESPONDE POR DAÑOS INDIRECTOS, INCIDENTALES, ESPECIALES, CONSECUENTES, EJEMPLARES O PUNITIVOS, NI POR PÉRDIDA DE DATOS, BENEFICIOS, INGRESOS, REPUTACIÓN O INTERRUPCIÓN, DERIVADOS DEL JUEGO.

EN LA MÁXIMA MEDIDA PERMITIDA, LA RESPONSABILIDAD TOTAL DE JESUS AFKERIAN NO SUPERARÁ EL MAYOR ENTRE LO QUE LE PAGASTE DIRECTAMENTE POR EL JUEGO DURANTE LOS DOCE MESES ANTERIORES AL HECHO O DIEZ DÓLARES ESTADOUNIDENSES. ESTE LÍMITE NO SE APLICA CUANDO LA LEY EXIGE OTRO RESULTADO.

17. INDEMNIZACIÓN LIMITADA

En la máxima medida permitida, defenderás, indemnizarás y mantendrás indemne a Jesus Afkerian frente a reclamaciones de terceros, daños, sentencias, pérdidas y costes razonables derivados de tu uso ilícito, incumplimiento material o contenido enviado por soporte que vulnere derechos ajenos.

Jesus Afkerian dará aviso razonablemente rápido y te permitirá controlar la defensa con abogado razonablemente aceptable. No podrás acordar una solución sin su consentimiento escrito previo si admite culpa suya, le impone una obligación no monetaria o no lo libera plenamente; el consentimiento no se denegará irrazonablemente. Puede participar con abogado propio a su cargo.

18. DERECHOS OBLIGATORIOS

Estos Términos no renuncian a protecciones del consumidor, derechos, remedios o reglas jurisdiccionales que legalmente no puedan renunciarse o limitarse.

19. LEY APLICABLE Y FORO

Estos Términos se rigen por la ley de Florida, sin considerar sus principios sobre conflicto de leyes, salvo cuando una norma obligatoria exija otra cosa. Sujeto a cualquier derecho irrenunciable a otro foro, los procedimientos deben presentarse ante los tribunales estatales ubicados en Orange County, Florida, o los tribunales federales que sirven a Orange County, Florida.

20. CAMBIOS

Jesus Afkerian puede actualizar estos Términos por cambios en el Juego, proveedores, riesgos o requisitos aplicables. Los Términos actualizados indicarán su fecha efectiva y los cambios materiales recibirán aviso razonablemente visible cuando corresponda.

La publicación por sí sola, el silencio, la inacción o mantener instalado el Juego no constituyen aceptación de Términos actualizados. El acceso o uso continuado después de un aviso razonablemente visible y la fecha efectiva indicada es la conducta en la que se basa el consentimiento, en la máxima medida permitida por la ley.

21. DISPOSICIONES GENERALES

Estos Términos, la Política de Privacidad y los avisos incorporados forman el acuerdo sobre el Juego. Si una disposición no es ejecutable, se aplicará hasta el máximo permitido y el resto continuará. No exigir una disposición no es renuncia. No puedes ceder estos Términos sin consentimiento escrito previo; Jesus Afkerian puede cederlos con una transferencia lícita del Juego o de sus intereses comerciales, sujeto a la ley.

22. CONTACTO

Jesus Afkerian
{CONTACT}
"""


BSD_TEXT = """Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.
    * Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

MIT_TEXT = """Checker Framework qualifiers
Copyright 2004-present by the Checker Framework developers

MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""


def third_party(product: dict[str, object], language: str) -> str:
    name = str(product["name"])
    if language == "es-419":
        inventory = "\n".join(f"- {item}" for item in product["inventory_es"])
        body = f"""1. FINALIDAD

Este documento identifica software, servicios y material de terceros usados por {name} (el «Juego»). Jesus Afkerian es la persona física que publica y opera el Juego. Los terceros conservan sus respectivos derechos y sus términos controlan sus propios materiales y servicios.

2. SERVICIOS DE GOOGLE

El Juego usa Google Mobile Ads, Google User Messaging Platform, Google Analytics for Firebase, Firebase Crashlytics, Firebase Installations y Firebase Sessions. Estos componentes están sujetos a los términos y políticas aplicables de Google. La Política de Privacidad explica su tratamiento de datos.

3. INVENTARIO CREATIVO Y DE SERVICIOS

{inventory}

Los avisos individuales accesibles desde la pantalla legal del Juego y desde la página legal del producto proporcionan la fuente y los términos aplicables. Ningún nombre de proveedor implica afiliación, patrocinio o respaldo.

4. SOFTWARE DEL RUNTIME RELEASE

El Juego distribuye componentes directos y transitivos de AndroidX, Kotlin, Jetpack Compose y otras bibliotecas. Los componentes de código abierto identificados se ofrecen principalmente bajo Apache License 2.0, con las excepciones reproducidas en las Secciones 5 y 6. El texto completo de Apache License 2.0 se ofrece en la página Apache License 2.0 del Juego.

Los SDK propietarios de Google y componentes relacionados están sujetos a los términos aplicables de Google, incluidos los Google Mobile Developer Services Terms y términos específicos del servicio; no se presentan como software Apache solo por usar una coordenada de Google.

5. DATASTORE EXTERNAL PROTOBUF — BSD 3-CLAUSE

El componente AndroidX DataStore Preferences External Protobuf incorpora material bajo BSD 3-Clause. El siguiente texto se reproduce sin traducir:

{BSD_TEXT}

6. CHECKER FRAMEWORK QUALIFIERS — MIT

El componente Checker Framework Qualifiers se distribuye bajo MIT. El siguiente texto se reproduce sin traducir:

{MIT_TEXT}

7. PRIVACIDAD, TÉRMINOS Y AUSENCIA DE RESPALDO

El uso del Juego también está sujeto a su Política de Privacidad y sus Términos del Servicio. Los proveedores identificados no operan, mantienen ni respaldan el Juego salvo que sus propios términos indiquen expresamente otra cosa.

8. CONTACTO

Jesus Afkerian
{CONTACT}
"""
        return header("AVISOS DE TERCEROS", name, language) + body

    inventory = "\n".join(f"- {item}" for item in product["inventory_en"])
    body = f"""1. PURPOSE

This document identifies third-party software, services, and materials used by {name} (the “Game”). Jesus Afkerian is the individual who publishes and operates the Game. Third parties retain their respective rights, and their terms control their own materials and services.

2. GOOGLE SERVICES

The Game uses Google Mobile Ads, Google User Messaging Platform, Google Analytics for Firebase, Firebase Crashlytics, Firebase Installations, and Firebase Sessions. These components are subject to applicable Google terms and policies. The Privacy Policy describes their information processing.

3. CREATIVE AND SERVICE INVENTORY

{inventory}

Individual notices available through the Game's legal screen and product legal page provide the relevant source and governing terms. Naming a provider does not imply affiliation, sponsorship, or endorsement.

4. RELEASE RUNTIME SOFTWARE

The Game distributes direct and transitive components from AndroidX, Kotlin, Jetpack Compose, and other libraries. Identified open-source components are offered primarily under the Apache License 2.0, with the exceptions reproduced in Sections 5 and 6. The complete Apache License 2.0 appears on the Game's Apache License 2.0 page.

Proprietary Google SDKs and related components are subject to applicable Google terms, including the Google Mobile Developer Services Terms and service-specific terms; they are not represented as Apache software merely because they use a Google coordinate.

5. DATASTORE EXTERNAL PROTOBUF — BSD 3-CLAUSE

The AndroidX DataStore Preferences External Protobuf component includes material under the BSD 3-Clause terms:

{BSD_TEXT}

6. CHECKER FRAMEWORK QUALIFIERS — MIT

The Checker Framework Qualifiers component is distributed under the MIT terms:

{MIT_TEXT}

7. PRIVACY, TERMS, AND NO ENDORSEMENT

Use of the Game is also subject to its Privacy Policy and Terms of Service. The providers identified here do not operate, maintain, or endorse the Game unless their own terms expressly state otherwise.

8. CONTACT

Jesus Afkerian
{CONTACT}
"""
    return header("THIRD-PARTY NOTICES", name, language) + body


def service_notice(title: str, product: str, body: str) -> str:
    return header(title, product, "en-US") + body.strip() + "\n"


def notice_documents() -> dict[str, str]:
    xo = PRODUCTS["xo-arcade"]["name"]
    air = PRODUCTS["air-strike-arcade"]["name"]
    tap = PRODUCTS["tap-odyssey"]["name"]
    admob = """1. SERVICE

The Game uses Google AdMob through the Google Mobile Ads SDK to display advertising and Google User Messaging Platform (“UMP”) to manage advertising eligibility and privacy messages.

2. INFORMATION PROCESSING

Google states that Mobile Ads automatically processes and shares IP address information that may estimate approximate location, Game and advertising interactions, diagnostic information, and device or account identifiers for advertising, analytics, and fraud prevention. The Game's Privacy Policy provides the product-specific disclosure.

3. USER CHOICES

Where Google reports that Privacy Options are required, the Game provides access to UMP Privacy Options. Android advertising controls and Google account controls may provide additional choices. These controls have different scopes and do not disable all Google services or all network activity.

4. TERMS AND POLICIES

Google Mobile Ads SDK disclosure:
https://developers.google.com/admob/android/privacy/play-data-disclosure

Google Mobile Ads SDK Terms:
https://developers.google.com/ad-manager/mobile-ads-sdk/terms

Google Privacy Policy:
https://policies.google.com/privacy

5. NO ENDORSEMENT

Google does not operate or endorse the Game merely because its services are integrated.
"""
    pixabay = """1. SOURCE

The Game includes sound effects obtained from Pixabay and integrated into its audiovisual experience.

Pixabay:
https://pixabay.com

2. GOVERNING TERMS

Pixabay content is subject to the Pixabay Content License and applicable Pixabay terms:
https://pixabay.com/service/license-summary/
https://pixabay.com/service/terms/

3. USE RESTRICTIONS

The sound effects are used only as integrated parts of the Game. They are not offered as a standalone stock library or as a substitute for the original content. The Pixabay license does not itself grant rights in trademarks, brands, recognizable people, or other third-party rights that may be associated with particular content.

4. ATTRIBUTION AND NO ENDORSEMENT

Attribution is not generally required by the Pixabay Content License. This source notice does not imply that Pixabay sponsors or endorses the Game.
"""
    suno = """1. SOURCE

The Game includes music generated using Suno.

Suno:
https://suno.com

2. GOVERNING TERMS

Use of Suno and generated output is governed by the terms and plan that applied when each track was generated. Suno states that commercial-use rights depend on generation during an eligible paid subscription and do not arise retroactively from a later subscription.

Suno Terms:
https://suno.com/terms

Suno commercial-use guidance:
https://help.suno.com/en/articles/9601665

3. RIGHTS AND RESTRICTIONS

This notice does not expand Suno's terms or grant a user the right to extract, redistribute, or separately exploit music from the Game. Suno's terms and applicable law control ownership and permitted use.

4. NO ENDORSEMENT

Suno does not sponsor or endorse the Game merely because its service was used.
"""
    eleven = """1. SOURCE

The Game includes voice or sound effects generated using ElevenLabs.

ElevenLabs:
https://elevenlabs.io

2. GOVERNING TERMS

Use of ElevenLabs and generated output is governed by the terms and subscription that applied when each output was generated. ElevenLabs states that paid plans may include commercial rights, while free-plan output is restricted, and beta services are subject to separate restrictions.

ElevenLabs Terms of Use:
https://elevenlabs.io/terms-of-use

ElevenLabs Beta Services Addendum:
https://elevenlabs.io/bsa

Publishing guidance:
https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform

3. RIGHTS AND RESTRICTIONS

This notice does not expand ElevenLabs' terms or grant a user the right to extract, redistribute, or separately exploit audio from the Game.

4. NO ENDORSEMENT

ElevenLabs does not sponsor or endorse the Game merely because its service was used.
"""
    kenney = """1. SOURCE

The Game includes sound effects from the Kenney Casino Audio and UI Audio packs:
https://kenney.nl/assets/casino-audio
https://kenney.nl/assets/ui-audio

2. LICENSE

Both pack pages identify the assets as Creative Commons CC0. The CC0 1.0 Universal legal code is:
https://creativecommons.org/publicdomain/zero/1.0/legalcode

CC0 does not grant trademark or patent rights and does not affect rights held by persons other than the person making the dedication.

3. ATTRIBUTION AND NO ENDORSEMENT

Attribution is not required under CC0. Source identification is provided for transparency. Kenney does not sponsor or endorse the Game.
"""
    openai = """1. SOURCE

The Game includes visual assets generated using OpenAI services for individuals, including ChatGPT.

OpenAI:
https://openai.com

2. GOVERNING TERMS AND OWNERSHIP

Use of the services and outputs is subject to the applicable OpenAI Terms of Use:
https://openai.com/policies/terms-of-use/

As between Jesus Afkerian and OpenAI, and to the extent permitted by applicable law, Jesus Afkerian retains his ownership rights in the inputs and owns the outputs as provided by the applicable OpenAI Terms. OpenAI assigns to Jesus Afkerian any right, title, and interest it may have in those outputs, subject to those Terms and applicable law.

3. SIMILAR OUTPUTS, REVIEW, AND THIRD-PARTY RIGHTS

Outputs may not be unique, and other users may receive similar output. OpenAI's assignment does not extend to another user's output or third-party material. Jesus Afkerian remains responsible for evaluating output accuracy and suitability and for obtaining any rights required for the Game's use.

4. NO ENDORSEMENT

OpenAI does not sponsor or endorse the Game merely because its service was used.

"""
    return {
        "xo-arcade/legal/AD_SERVICES_NOTICE.txt": service_notice("GOOGLE ADMOB AND UMP NOTICE", str(xo), admob),
        "air-strike-arcade/legal/AD_SERVICES_NOTICE.txt": service_notice("GOOGLE ADMOB AND UMP NOTICE", str(air), admob),
        "tap-odyssey/legal/AD_SERVICES_NOTICE.txt": service_notice("GOOGLE ADMOB AND UMP NOTICE", str(tap), admob),
        "air-strike-arcade/legal/PIXABAY_NOTICE.txt": service_notice("PIXABAY SOUND EFFECTS NOTICE", str(air), pixabay),
        "tap-odyssey/legal/PIXABAY_NOTICE.txt": service_notice("PIXABAY SOUND EFFECTS NOTICE", str(tap), pixabay),
        "xo-arcade/legal/SUNO_NOTICE.txt": service_notice("SUNO GENERATED MUSIC NOTICE", str(xo), suno),
        "air-strike-arcade/legal/SUNO_NOTICE.txt": service_notice("SUNO GENERATED MUSIC NOTICE", str(air), suno),
        "tap-odyssey/legal/SUNO_NOTICE.txt": service_notice("SUNO GENERATED MUSIC NOTICE", str(tap), suno),
        "xo-arcade/legal/ELEVENLABS_NOTICE.txt": service_notice("ELEVENLABS GENERATED AUDIO NOTICE", str(xo), eleven),
        "xo-arcade/legal/KENNEY_NOTICE.txt": service_notice("KENNEY ASSET NOTICE — CC0 1.0", str(xo), kenney),
        "tap-odyssey/legal/OPENAI_CHATGPT_NOTICE.txt": service_notice("OPENAI / CHATGPT GENERATED ASSET NOTICE", str(tap), openai),
    }


def website_privacy(language: str) -> str:
    if language == "es-419":
        return header("POLÍTICA DE PRIVACIDAD", "SITIO PÚBLICO DE JESUS AFKERIAN", language) + f"""1. ALCANCE

Esta Política explica cómo Jesus Afkerian, persona física que publica y opera este sitio, trata información relacionada con el sitio público. No rige las apps o juegos, que tienen políticas propias enlazadas desde sus páginas.

2. ALOJAMIENTO Y REGISTROS TÉCNICOS

El sitio es estático y se aloja mediante GitHub Pages. Al solicitar una página, GitHub y proveedores de red pueden recibir dirección IP, fecha y hora, recurso solicitado, agente de usuario, información del dispositivo o navegador, datos de referencia y diagnósticos de seguridad o entrega. Jesus Afkerian no controla los registros propios de GitHub.

GitHub Privacy Statement:
https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement

3. COOKIES, ANALÍTICA Y FORMULARIOS

Jesus Afkerian no incorpora en este sitio una cuenta propia, formulario web, publicidad, píxel de marketing ni analítica web propia. El alojamiento y los enlaces externos pueden operar bajo políticas independientes.

4. CORREO

Si escribes a soporte, Jesus Afkerian recibe tu dirección, mensaje, adjuntos y cualquier información que decidas enviar. Se usa para responder, mantener registros apropiados, prevenir abuso, resolver disputas y proteger derechos.

5. ENLACES EXTERNOS

Los enlaces a Google Play, Google, GitHub, proveedores y otras páginas llevan a servicios independientes. Sus operadores controlan su tratamiento de datos.

6. CONSERVACIÓN Y DIVULGACIÓN

El correo se conserva durante el tiempo razonablemente necesario para gestionar la solicitud, mantener registros, prevenir abuso, resolver disputas y cumplir obligaciones legales. Puede conservarse o divulgarse información cuando sea razonablemente necesario ante proceso legal válido, incidentes de seguridad o para establecer, ejercer o defender reclamaciones.

7. DERECHOS Y SOLICITUDES

Según tu residencia, la ley aplicable, umbrales y excepciones, puedes tener derechos sobre información personal. Envía solicitudes a {CONTACT}. Puede requerirse información razonablemente necesaria para verificar y responder.

8. SEGURIDAD

Se usan medidas razonables apropiadas para la información controlada, pero ningún método de almacenamiento o transmisión es completamente seguro.

9. NIÑOS

El sitio presenta productos destinados a adultos y no se dirige a niños. Si crees que un niño envió información por correo, contacta a Jesus Afkerian.

10. CAMBIOS

Esta Política puede actualizarse cuando cambien el sitio, el alojamiento o requisitos aplicables. El documento actualizado indicará su fecha efectiva.

11. CONTACTO

Jesus Afkerian
{CONTACT}
"""
    return header("PRIVACY POLICY", "JESUS AFKERIAN PUBLIC WEBSITE", language) + f"""1. SCOPE

This Policy explains how Jesus Afkerian, the individual who publishes and operates this website, processes information related to the public website. It does not govern the apps or games, which have product-specific policies linked from their pages.

2. HOSTING AND TECHNICAL LOGS

The website is static and hosted through GitHub Pages. When a page is requested, GitHub and network providers may receive an IP address, date and time, requested resource, user agent, browser or device information, referring information, and security or delivery diagnostics. Jesus Afkerian does not control GitHub's independent logs.

GitHub Privacy Statement:
https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement

3. COOKIES, ANALYTICS, AND FORMS

Jesus Afkerian does not embed a first-party account, web form, advertising service, marketing pixel, or first-party web analytics service on this website. Hosting infrastructure and external links may operate under independent policies.

4. EMAIL

If you contact support, Jesus Afkerian receives your email address, message, attachments, and any other information you choose to send. It is used to respond, keep appropriate records, prevent abuse, resolve disputes, and protect rights.

5. EXTERNAL LINKS

Links to Google Play, Google, GitHub, providers, and other pages lead to independent services. Their operators control their own information processing.

6. RETENTION AND DISCLOSURE

Email is retained for the time reasonably necessary to handle the request, keep appropriate records, prevent abuse, resolve disputes, and meet legal obligations. Information may be preserved or disclosed when reasonably necessary in response to valid legal process, security incidents, or to establish, exercise, or defend legal claims.

7. RIGHTS AND REQUESTS

Depending on your residence, applicable law, thresholds, and exceptions, you may have rights concerning personal information. Send requests to {CONTACT}. Information reasonably necessary to verify and answer the request may be required.

8. SECURITY

Reasonable measures appropriate to the information controlled are used, but no storage or transmission method is completely secure.

9. CHILDREN

The website presents products intended for adults and is not directed to children. If you believe a child sent information by email, contact Jesus Afkerian.

10. CHANGES

This Policy may be updated when the website, hosting, or applicable requirements change. The updated document will state its effective date.

11. CONTACT

Jesus Afkerian
{CONTACT}
"""


def website_terms(language: str) -> str:
    if language == "es-419":
        return header("TÉRMINOS DEL SERVICIO", "SITIO PÚBLICO DE JESUS AFKERIAN", language) + f"""1. ALCANCE Y ACUERDO

Estos Términos del Servicio son un acuerdo entre tú y Jesus Afkerian, persona física que publica y opera este sitio. Rigen tu acceso y uso del sitio. Los juegos tienen términos separados.

2. FINALIDAD INFORMATIVA

El sitio proporciona información sobre productos y documentación pública. No constituye asesoría legal, financiera, médica ni profesional, ni garantiza que un producto esté disponible en una región o dispositivo.

3. LICENCIA DEL SITIO

Sujeto a estos Términos, puedes acceder y visualizar el sitio para fines personales y lícitos. No se transfiere propiedad ni se concede licencia para copiar, explotar comercialmente, extraer de forma masiva o reutilizar marcas, imágenes o contenido salvo permiso expreso o ley aplicable.

4. PROPIEDAD Y TERCEROS

Jesus Afkerian y sus licenciantes conservan sus respectivos derechos. Los nombres, marcas y materiales de terceros pertenecen a sus titulares y se rigen por sus términos.

5. CONDUCTA PROHIBIDA

No puedes interferir con el sitio, introducir código malicioso, eludir controles, realizar solicitudes automatizadas perjudiciales, falsear afiliación, vulnerar derechos ajenos ni usar el sitio ilegalmente.

6. SERVICIOS EXTERNOS

GitHub Pages, Google Play y otros destinos enlazados son independientes. Jesus Afkerian no controla su disponibilidad, seguridad, contenido ni tratamiento de datos.

7. DISPONIBILIDAD Y CAMBIOS

El sitio puede corregirse, cambiarse, suspenderse o discontinuarse. No se promete disponibilidad ininterrumpida ni ausencia de errores.

8. PRIVACIDAD

La Política de Privacidad del sitio explica el alojamiento, correo y enlaces:
https://afkerianinteractive.github.io/privacy-policy-es.html

9. EXCLUSIONES DE GARANTÍAS

EN LA MÁXIMA MEDIDA PERMITIDA, EL SITIO SE OFRECE «TAL CUAL» Y «SEGÚN DISPONIBILIDAD». SE EXCLUYEN GARANTÍAS IMPLÍCITAS QUE LEGALMENTE PUEDAN EXCLUIRSE. NADA EXCLUYE DERECHOS O REMEDIOS IRRENUNCIABLES.

10. LIMITACIÓN DE RESPONSABILIDAD

EN LA MÁXIMA MEDIDA PERMITIDA, JESUS AFKERIAN NO RESPONDE POR DAÑOS INDIRECTOS, INCIDENTALES, ESPECIALES, CONSECUENTES, EJEMPLARES O PUNITIVOS, NI POR PÉRDIDA DE DATOS, BENEFICIOS, INGRESOS O REPUTACIÓN DERIVADA DEL SITIO.

La responsabilidad total no superará diez dólares estadounidenses, salvo cuando la ley exija otro resultado.

11. INDEMNIZACIÓN LIMITADA

En la máxima medida permitida, indemnizarás a Jesus Afkerian por reclamaciones de terceros derivadas de tu uso ilícito, incumplimiento material o vulneración de derechos ajenos. Recibirás aviso razonablemente rápido y podrás controlar la defensa con abogado razonablemente aceptable. No podrás acordar una solución sin consentimiento escrito previo si admite culpa, impone una obligación no monetaria o no libera plenamente a Jesus Afkerian; el consentimiento no se denegará irrazonablemente.

12. DERECHOS OBLIGATORIOS

Nada renuncia a protecciones, derechos, remedios o reglas jurisdiccionales que no puedan renunciarse o limitarse.

13. LEY APLICABLE Y FORO

Estos Términos se rigen por la ley de Florida, sin considerar sus principios sobre conflicto de leyes, salvo cuando una norma obligatoria exija otra cosa. Sujeto a cualquier derecho irrenunciable a otro foro, los procedimientos deben presentarse ante los tribunales estatales ubicados en Orange County, Florida, o los tribunales federales que sirven a Orange County, Florida.

14. CAMBIOS

Los Términos actualizados indicarán su fecha efectiva y los cambios materiales recibirán aviso razonablemente visible cuando corresponda. La publicación por sí sola, el silencio o la inacción no constituyen aceptación; el uso continuado después del aviso y la fecha efectiva es la conducta en que se basa el consentimiento, en la máxima medida permitida.

15. DISPOSICIONES GENERALES

Si una disposición no es ejecutable, se aplicará hasta el máximo permitido y el resto continuará. No exigir una disposición no constituye renuncia.

16. CONTACTO

Jesus Afkerian
{CONTACT}
"""
    return header("TERMS OF SERVICE", "JESUS AFKERIAN PUBLIC WEBSITE", language) + f"""1. SCOPE AND AGREEMENT

These Terms of Service are an agreement between you and Jesus Afkerian, the individual who publishes and operates this website. They govern access to and use of the website. The games have separate terms.

2. INFORMATIONAL PURPOSE

The website provides product information and public documentation. It is not legal, financial, medical, or other professional advice and does not promise that a product is available in any region or on any device.

3. WEBSITE LICENSE

Subject to these Terms, you may access and view the website for personal and lawful purposes. No ownership is transferred, and no license is granted to copy, commercially exploit, scrape in bulk, or reuse marks, images, or content except with express permission or as allowed by law.

4. OWNERSHIP AND THIRD PARTIES

Jesus Afkerian and his licensors retain their respective rights. Third-party names, marks, and materials belong to their owners and are subject to their terms.

5. PROHIBITED CONDUCT

You may not interfere with the website, introduce malicious code, evade controls, make harmful automated requests, misrepresent affiliation, violate another person's rights, or use the website unlawfully.

6. EXTERNAL SERVICES

GitHub Pages, Google Play, and other linked destinations are independent. Jesus Afkerian does not control their availability, security, content, or information processing.

7. AVAILABILITY AND CHANGES

The website may be corrected, changed, suspended, or discontinued. Uninterrupted or error-free availability is not promised.

8. PRIVACY

The website Privacy Policy explains hosting, email, and external links:
https://afkerianinteractive.github.io/privacy-policy.html

9. DISCLAIMERS

TO THE MAXIMUM EXTENT PERMITTED BY LAW, THE WEBSITE IS PROVIDED “AS IS” AND “AS AVAILABLE.” IMPLIED WARRANTIES THAT MAY LAWFULLY BE EXCLUDED ARE DISCLAIMED. NOTHING EXCLUDES A NONWAIVABLE RIGHT OR REMEDY.

10. LIMITATION OF LIABILITY

TO THE MAXIMUM EXTENT PERMITTED BY LAW, JESUS AFKERIAN WILL NOT BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES, OR FOR LOSS OF DATA, PROFITS, REVENUE, OR GOODWILL ARISING FROM THE WEBSITE.

Aggregate liability will not exceed ten U.S. dollars unless applicable law requires another result.

11. NARROW INDEMNITY

To the maximum extent permitted by law, you will indemnify Jesus Afkerian against third-party claims arising from your unlawful use, material breach, or violation of another person's rights. You will receive reasonably prompt notice and may control the defense with counsel reasonably acceptable to him. You may not settle without prior written consent if the settlement admits fault, imposes a nonmonetary obligation, or does not fully release Jesus Afkerian; consent will not be unreasonably withheld.

12. MANDATORY RIGHTS

Nothing waives protections, rights, remedies, or jurisdictional rules that cannot lawfully be waived or limited.

13. GOVERNING LAW AND VENUE

These Terms are governed by Florida law, without regard to conflict-of-laws principles, except where mandatory law requires otherwise. Subject to any nonwaivable right to another forum, proceedings must be brought in the state courts located in Orange County, Florida, or the federal courts serving Orange County, Florida.

14. CHANGES

Updated Terms will state their effective date and material changes will receive reasonably conspicuous notice where appropriate. Publication alone, silence, or inaction does not constitute acceptance; continued use after notice and the effective date is the conduct relied upon as assent, to the maximum extent permitted by law.

15. GENERAL

If a provision is unenforceable, it will be enforced to the maximum lawful extent and the remainder will continue. Failure to enforce a provision is not a waiver.

16. CONTACT

Jesus Afkerian
{CONTACT}
"""


def territory(language: str) -> str:
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
        "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
        "West Virginia", "Wisconsin", "Wyoming", "District of Columbia",
    ]
    bullets = "\n".join(f"- {state}" for state in states)
    if language == "es-419":
        return header("TERRITORIO PERMITIDO", "JUEGOS PUBLICADOS POR JESUS AFKERIAN", language) + f"""Esta lista define el territorio actualmente autorizado por Jesus Afkerian para XO Arcade: Infinity Edition, Air Strike Arcade y Tap Odyssey. La disponibilidad técnica o pública fuera de esta lista no concede autorización.

Subjurisdicciones permitidas de Estados Unidos:

{bullets}

Quedan fuera los territorios y posesiones de Estados Unidos y cualquier país o región no enumerado. La disponibilidad real de Google Play depende además de la configuración de publicación controlada por el propietario.
"""
    return header("PERMITTED TERRITORY", "GAMES PUBLISHED BY JESUS AFKERIAN", language) + f"""This list defines the territory currently authorized by Jesus Afkerian for XO Arcade: Infinity Edition, Air Strike Arcade, and Tap Odyssey. Technical or public accessibility outside this list does not grant authorization.

Permitted United States subjurisdictions:

{bullets}

United States territories and possessions, and every country or region not listed, are excluded. Actual Google Play availability also depends on owner-controlled publishing configuration.
"""


def write(path: str, value: str) -> None:
    target = (ROOT / path).resolve()
    target.relative_to(ROOT)
    target.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    for slug, product in PRODUCTS.items():
        write(f"{slug}/legal/PRIVACY_POLICY.txt", privacy_en(product))
        write(f"{slug}/legal/PRIVACY_POLICY_ES.txt", privacy_es(product))
        write(f"{slug}/legal/TERMS_OF_SERVICE.txt", terms_en(product))
        write(f"{slug}/legal/TERMS_OF_SERVICE_ES.txt", terms_es(product))
        write(f"{slug}/legal/THIRD_PARTY_NOTICES.txt", third_party(product, "en-US"))
        write(f"{slug}/legal/THIRD_PARTY_NOTICES_ES.txt", third_party(product, "es-419"))

    for path, value in notice_documents().items():
        write(path, value)

    write("legal/WEBSITE_PRIVACY_POLICY.txt", website_privacy("en-US"))
    write("legal/WEBSITE_PRIVACY_POLICY_ES.txt", website_privacy("es-419"))
    write("legal/WEBSITE_TERMS_OF_SERVICE.txt", website_terms("en-US"))
    write("legal/WEBSITE_TERMS_OF_SERVICE_ES.txt", website_terms("es-419"))
    write("legal/PERMITTED_TERRITORY.txt", territory("en-US"))
    write("legal/PERMITTED_TERRITORY_ES.txt", territory("es-419"))

    print("Rewrote 35 first-party legal TXT documents; upstream licenses unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
