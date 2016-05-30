#Snippets from standards

(https://tools.ietf.org/html/draft-sweet-rfc2910bis-07)

3.1.1.  Request and Response

   An operation request or response is encoded as follows:

      -----------------------------------------------
      |                  version-number             |   2 bytes  - required
      -----------------------------------------------
      |               operation-id (request)        |
      |                      or                     |   2 bytes  - required
      |               status-code (response)        |
      -----------------------------------------------
      |                   request-id                |   4 bytes  - required
      -----------------------------------------------
      |                 attribute-group             |   n bytes - 0 or more
      -----------------------------------------------
      |              end-of-attributes-tag          |   1 byte   - required
      -----------------------------------------------
      |                     data                    |   q bytes  - optional
      -----------------------------------------------


   (http://tools.ietf.org/html/rfc2567#section-5.2)

   The protocol must handle overrun conditions in the printer and must
   support overlapped printing and downloading of the file in devices
   that are unable to spool files before printing them.

   Every print request will have a response. Responses will indicate
   success or failure of the request and provide information on failures
   when they occur. Responses would include things like:

   - Got the print job and queued it
   - Got the print job and am printing it
   - Got the print job, started to print it, but printing failed
      - why it failed (e.g. unrecoverable PostScript error)
      - state of the printer
      - how much printed
   - Got the print job but couldn't print it
      - why it can't be printed
      - state of the printer
   - Got the print job but don't know what to do with it
   - Didn't get a complete print job (e.g. communication failure)



5.5. ASYNCHRONOUS NOTIFICATION

   Client                                               IPP Printer

    +----------------------------------------------------------- >
       Use the following method to notify me of Printer events

                                 .
                                 .
                                 .
    < -----------------------------------------------------------+
        Asynchronous notification of Printer event

   Clients must be able to request asynchronous notification for Printer
   events such as

   - job completion
   - a fatal error that requires the job to be resubmitted
   - a condition that severely impacts a queued job for this client
      e.g. printer is out of paper

   Note: end-user notification is a V1.0 design goal while operator
   notification is for V2.0.



http://tools.ietf.org/html/rfc2911

                                   +--------------+
                                   |  Application |
                         o         +. . . . . . . |
                        \|/        |   Spooler    |
                        / \        +. . . . . . . |   +---------+
                      End-User     | Print Driver |---|  File   |
            +-----------+ +-----+  +------+-------+   +----+----+
            |  Browser  | | GUI |         |                |
            +-----+-----+ +--+--+         |                |
                  |          |            |                |
                  |      +---+------------+---+            |
      N   D   S   |      |      IPP Client    |------------+
      O   I   E   |      +---------+----------+
      T   R   C   |                |
      I   E   U   |
      F   C   R   -------------- Transport ------------------
      I   T   I
      C   O   T                    |         --+
      A   R   Y           +--------+--------+  |
      T   Y               |    IPP Server   |  |
      I                   +--------+--------+  |
      O                            |           |
      N                   +-----------------+  | IPP Printer
                          |  Print Service  |  |
                          +-----------------+  |
                                   |         --+
                          +-----------------+
                          | Output Device(s)|
                          +-----------------+


### Types of IPP Printer


RFC 2911              IPP/1.1: Model and Semantics        September 2000

*Fan out* is a print server.


      embedded printer:
                                                output device
                                              +---------------+
       O   +--------+                         |  ###########  |
      /|\  | client |------------IPP------------># Printer #  |
      / \  +--------+                         |  # Object  #  |
                                              |  ###########  |
                                              +---------------+

      hosted printer:
                                              +---------------+
       O   +--------+        ###########      |               |
      /|\  | client |--IPP--># Printer #-any->| output device |
      / \  +--------+        # Object  #      |               |
                             ###########      +---------------+


                                               +---------------+
      fan out:                                 |               |
                                           +-->| output device |
                                       any/    |               |
       O   +--------+      ###########   /     +---------------+
      /|\  | client |-IPP-># Printer #--*
      / \  +--------+      # Object  #   \     +---------------+
                           ########### any\    |               |
                                           +-->| output device |
                                               |               |
                                               +---------------+

Hastings, et al.            Standards Track                    [Page 15]

RFC 2911              IPP/1.1: Model and Semantics        September 2000

2.2 Job Object

   A Job object is used to model a print job.  A Job object contains
   documents.  The information required to create a Job object is sent
   in a create request from the end user via an IPP Client to the
   Printer object.  The Printer object validates the create request, and
   if the Printer object accepts the request, the Printer object creates
   the new Job object.  Section 3 describes each of the Job operations
   in detail.

   The characteristics and state of a Job object are described by its
   attributes.  Job attributes are grouped into two groups as follows:

      - "job-template" attributes: These attributes can be supplied by
        the client or end user and include job processing instructions
        which are intended to override any Printer object defaults
        and/or instructions embedded within the document data. (See
        section 4.2)

      - "job-description" attributes: These attributes describe the Job
        object's identification, state, size, etc. The client supplies
        some of these attributes, and the Printer object generates
        others. (See section 4.3)

   An implementation MUST support at least one document per Job object.
   An implementation MAY support multiple documents per Job object.  A
   document is either:

      - a stream of document data in a format supported by the Printer
        object (typically a Page Description Language - PDL), or
      - a reference to such a stream of document data    !@#$ Needed?

   In IPP/1.1, a document is not modeled as an IPP object, therefore it
   has no object identifier or associated attributes.  All job
   processing instructions are modeled as Job object attributes.  These
   attributes are called Job Template attributes and they apply equally
   to all documents within a Job object.   !@#$ Document(s) or reference to it is part of job.

2.3 Object Relationships

   IPP objects have relationships that are maintained persistently along
   with the persistent storage of the object attributes.

   A Printer object can represent either one or more physical output
   devices or a logical device which "processes" jobs but never actually
   uses a physical output device to put marks on paper.  Examples of
   logical devices include a Web page publisher or a gateway into an
   online document archive or repository.  A Printer object contains
   zero or more Job objects.

   A Job object is contained by exactly one Printer object, however the
   identical document data associated with a Job object could be sent to
   either the same or a different Printer object.  In this case, a
   second Job object would be created which would be almost identical to
   the first Job object, however it would have new (different) Job
   object identifiers (see section 2.4).

   A Job object is either empty (before any documents have been added)
   or contains one or more documents.  If the contained document is a
   stream of document data, that stream can be contained in only one
   document.  However, there can be identical copies of the stream in
   other documents in the same or different Job objects.  If the
   contained document is just a reference to a stream of document data,
   other documents (in the same or different Job object(s)) may contain
   the same reference.

Hastings, et al.            Standards Track                    [Page 17]

RFC 2911              IPP/1.1: Model and Semantics        September 2000


   IPP/1.1 does not specify how the client obtains the client supplied
   URI, but it is RECOMMENDED that a Printer object be registered as an
   entry in a directory service.  End-users and programs can then
   interrogate the directory searching for Printers. Section 16 defines
   a generic schema for Printer object entries in the directory service
   and describes how the entry acts as a bridge to the actual IPP
   Printer object.  The entry in the directory that represents the IPP
   Printer object includes the possibly many URIs for that Printer
   object as values in one its attributes.


RFC 2911              IPP/1.1: Model and Semantics        September 2000


   IPP/1.1 does not specify how the client obtains the client supplied
   URI, but it is RECOMMENDED that a Printer object be registered as an
   entry in a directory service.  End-users and programs can then
   interrogate the directory searching for Printers. Section 16 defines
   a generic schema for Printer object entries in the directory service
   and describes how the entry acts as a bridge to the actual IPP
   Printer object.  The entry in the directory that represents the IPP
   Printer object includes the possibly many URIs for that Printer
   object as values in one its attributes.

   When a client submits a create request to the Printer object, the
   Printer object validates the request and creates a new Job object.
   The Printer object assigns the new Job object a URI which is stored
   in the "job-uri" Job attribute.  This URI is then used by clients as
   the target for subsequent Job operations.  The Printer object
   generates a Job URI based on its configured security policy and the
   URI used by the client in the create request.

   In addition, the Printer object also populates the Job object's
   "job-printer-uri" attribute.  This is a reference back to the Printer
   object that created the Job object.  If a client only has access to a
   Job object's "job-uri" identifier, the client can query the Job's
   "job-printer-uri" attribute in order to determine which Printer
   object created the Job object.  If the Printer object supports more
   than one URI, the Printer object picks the one URI supplied by the
   client when creating the job to build the value for and to populate
   the Job's "job-printer-uri" attribute.
   e.g. 'job-printer-uri', 'ipp://printserver-1.him.Uni-Mainz.DE:631/printers/GlobalA3'
        'IPP_TAG_URI', 'IPP_TAG_JOB'

   The Job ID (stored in the "job-id" attribute) only has meaning in the
   context of the Printer object to which the create request was
   originally submitted.

   e.g. 'job-id', 19, 'IPP_TAG_INTEGER', 'IPP_TAG_JOB'


   RFC 2911  IPP/1.1: Model and Semantics [Page 18]
   To summarize:

      - Each Printer object is identified with one or more URIs.  The
        Printer's "printer-uri-supported" attribute contains the URI(s).
      - The Printer object's "uri-security-supported" attribute
        identifies the communication channel security protocols that may
        or may not have been configured for the various Printer object
        URIs (e.g., 'tls' or 'none').
      - The Printer object's "uri-authentication-supported" attribute
        identifies the authentication mechanisms that may or may not
        have been configured for the various Printer object URIs (e.g.,
        'digest' or 'none').
      - Each Job object is identified with a Job URI.  The Job's "job-
        uri" attribute contains the URI.
      - Each Job object is also identified with Job ID which is a 32-
        bit, positive integer.  The Job's "job-id" attribute contains
        the Job ID.  The Job ID is only unique within the context of the
        Printer object  which created the Job object.
      - Each Job object has a "job-printer-uri" attribute which contains
        the URI of the Printer object that was used to create the Job
        object.  This attribute is used to determine the Printer object
        that created a Job object when given only the URI for the Job
        object.  This linkage is necessary to determine the languages,
        charsets, and operations which are supported on that Job (the
        basis for such support comes from the creating Printer object).
      - Each Printer object has a name (which is not necessarily
        unique).  The administrator chooses and sets this name through
        some mechanism outside the scope of this IPP/1.1 document.  The
        Printer object's "printer-name" attribute contains the name.
      - Each Job object has a name (which is not necessarily unique).
        The client optionally supplies this name in the create request.
        If the client does not supply this name, the Printer object
        generates a name for the Job object. The Job object's "job-name"
        attribute contains the name.


###3. IPP Operations

   IPP objects support operations.  An operation consists of a request
   and a response.  When a client communicates with an IPP object, the
   client issues an operation request to the URI for that object.
   Operation requests and responses have parameters that identify the
   operation.  Operations also have attributes that affect the run-time
   characteristics of the operation (the intended target, localization
   information, etc.).  These operation-specific attributes are called
   operation attributes (as compared to object attributes such as
   Printer object attributes or Job object attributes).  Each request
   carries along with it any operation attributes, object attributes,
   and/or document data required to perform the operation.  Each request
   requires a response from the object.  Each response indicates success
   or failure of the operation with a status code as a response
   parameter.  The response contains any operation attributes, object
   attributes, and/or status messages generated during the execution of
   the operation request.

   This section describes the semantics of the IPP operations, both
   requests and responses, in terms of the parameters, attributes, and
   other data associated with each operation.

 The IPP/1.1 Printer operations are:

     Print-Job (section 3.2.1)
     Print-URI (section 3.2.2)
     Validate-Job (section 3.2.3)
     Create-Job (section 3.2.4)
     Get-Printer-Attributes (section 3.2.5)
     Get-Jobs (section 3.2.6)
     Pause-Printer (section 3.3.5)
     Resume-Printer (section 3.3.6)
     Purge-Jobs (section 3.3.7)

   The Job operations are:

     Send-Document (section 3.3.1)
     Send-URI (section 3.3.2)
     Cancel-Job (section 3.3.3)
     Get-Job-Attributes (section 3.3.4)
     Hold-Job (section 3.3.5)
     Release-Job (section 3.3.6)
     Restart-Job (section 3.3.7)

   The Send-Document and Send-URI Job operations are used to add a new
   document to an existing multi-document Job object created using the
   Create-Job operation.


### 3.1.1 Required Parameters

   Every operation request contains the following REQUIRED parameters:

      - a "version-number",
      - an "operation-id",
      - a "request-id", and
      - the attributes that are REQUIRED for that type of request.

   Every operation response contains the following REQUIRED parameters:

      - a "version-number",
      - a "status-code",
      - the "request-id" that was supplied in the corresponding request,
        and
      - the attributes that are REQUIRED for that type of response.

### 3.1.2 Operation IDs and Request IDs

   Each IPP operation request includes an identifying "operation-id"
   value.  Valid values are defined in the "operations-supported"
   Printer attribute section (see section [4.4.15](http://tools.ietf.org/html/rfc2911#section-4.4.15)).
   The client specifies
   which operation is being requested by supplying the correct
   "operation-id" value.

   In addition, every invocation of an operation is identified by a
   "request-id" value. For each request, the client chooses the
   "request-id" which MUST be an integer (possibly unique depending on
   client requirements) in the range from 1 to 2**31 - 1 (inclusive).
   This "request-id" allows clients to manage multiple outstanding
   requests. The receiving IPP object copies all 32-bits of the client-
   supplied "request-id" attribute into the response so that the client
   can match the response with the correct outstanding request, even if
   the "request-id" is out of range.  If the request is terminated
   before the complete "request-id" is received, the IPP object rejects
   the request and returns a response with a "request-id" of 0.

   Note: In some cases, the transport protocol underneath IPP might be a
   connection oriented protocol that would make it impossible for a
   client to receive responses in any order other than the order in
   which the corresponding requests were sent.  In such cases, the
   "request-id" attribute would not be essential for correct protocol
   operation.  However, in other mappings, the operation responses can
   come back in any order.  In these cases, the "request-id" would be
   essential.

RFC 2911     IPP/1.1: Model and Semantics  [Page 22]

### 3.1.3 Attributes

   Operation requests and responses are both composed of groups of
   attributes and/or document data.  The attributes groups are:

      - Operation Attributes: These attributes are passed in the
        operation and affect the IPP object's behavior while processing
        the operation request and may affect other attributes or groups
        of attributes.  Some operation attributes describe the document
        data associated with the print job and are associated with new
        Job objects, however most operation attributes do not persist
        beyond the life of the operation.  The description of each
        operation attribute includes conformance statements indicating
        which operation attributes are REQUIRED and which are OPTIONAL
        for an IPP object to support and which attributes a client MUST
        supply in a request and an IPP object MUST supply in a response.
      - Job Template Attributes: These attributes affect the processing
        of a job.  A client OPTIONALLY supplies Job Template Attributes
        in a create request, and the receiving object MUST be prepared
        to receive all supported attributes.  The Job object can later
        be queried to find out what Job Template attributes were
        originally requested in the create request, and such attributes
        are returned in the response as Job Object Attributes.  The
        Printer object can be queried about its Job Template attributes
        to find out what type of job processing capabilities are
        supported and/or what the default job processing behaviors are,
        though such attributes are returned in the response as Printer
        Object Attributes.  The "ipp-attribute-fidelity" operation
        attribute affects processing of all client-supplied Job Template
        attributes (see sections 3.2.1.2 and 15 for a full description
        of "ipp-attribute-fidelity" and its relationship to other
        attributes).
      - Job Object Attributes: These attributes are returned in response
        to a query operation directed at a Job object.
      - Printer Object Attributes: These attributes are returned in
        response to a query operation directed at a Printer object.
      - Unsupported Attributes: In a create request, the client supplies
        a set of Operation and Job Template attributes.  If any of these
        attributes or their values is unsupported by the Printer object,
        the Printer object returns the set of unsupported attributes in
        the response.  Sections 3.1.7, 3.2.1.2, and  15 give a full
        description of how Job Template attributes supplied by the
        client in a create request are processed by the Printer object
        and how unsupported attributes are returned to the client.
        Because of extensibility, any IPP object might receive a request
        that contains new or unknown attributes or values for which it
        has no support. In such cases, the IPP object processes what it
        can and returns the unsupported attributes in the response. The
        Unsupported Attribute group is defined for all operation
        responses for returning unsupported attributes that the client
        supplied in the request.



### 3.1.4.1 Request Operation Attributes
         All clients and IPP objects MUST support the 'utf-8' charset
         [RFC2279] and MAY support additional charsets provided that
         they are registered with IANA [IANA-CS].


RFC 2911 IPP/1.1: Model and Semantics [Page 31]


### 3.1.6 Operation Response Status Codes and Status Messages

   Every operation response includes a REQUIRED "status-code" parameter
   and an OPTIONAL "status-message" operation attribute, and an OPTIONAL
   "detailed-status-message" operation attribute.  The Print-URI and
   Send-URI response MAY include an OPTIONAL "document-access-error"
   operation attribute.

3.1.6.1 "status-code" (type2 enum)

   The REQUIRED "status-code" parameter provides information on the
   processing of a request.

   The status code is intended for use by automata.  A client
   implementation of IPP SHOULD convert status code values into any
   localized message that has semantic meaning to the end user.

   The "status-code" value is a numeric value that has semantic meaning.
   The "status-code" syntax is similar to a "type2 enum" (see section
   4.1 on "Attribute Syntaxes") except that values can range only from
   0x0000 to 0x7FFF.  Section 13 describes the status codes, assigns the
   numeric values, and suggests a corresponding status message for each
   status code for use by the client when the user's natural language is
   English.

   If the Printer performs an operation with no errors and it encounters
   no problems, it MUST return the status code 'successful-ok' in the
   response.  See section 13.

   If the client supplies unsupported values for the following
   parameters or Operation attributes, the Printer object MUST reject
   the operation, NEED NOT return the unsupported attribute value in the
   Unsupported Attributes group, and MUST return the indicated status
   code:

        Parameter/Attribute                 Status code

        version-number      server-error-version-not-supported
        operation-id        server-error-operation-not-supported
        attributes-charset  client-error-charset-not-supported
        compression         client-error-compression-not-supported
        document-format     client-error-document-format-not-supported
        document-uri        client-error-uri-scheme-not-supported,
                             client-error-document-access-error

   If the client supplies unsupported values for other attributes, or
   unsupported attributes, the Printer returns the status code defined
   in section 3.1.7 on Unsupported Attributes.


### 3.1.9 Job Creation Operations

   In order to "submit a print job" and create a new Job object, a
   client issues a create request.  A create request is any one of
   following three operation requests:

      - The Print-Job Request: A client that wants to submit a print job
        with only a single document uses the Print-Job operation.  The
        operation allows for the client to "push" the document data to
        the Printer object by including the document data in the request
        itself.

      - The Print-URI Request: A client that wants to submit a print job
        with only a single document (where the Printer object "pulls"
        the document data instead of the client "pushing" the data to
        the Printer object) uses the Print-URI operation.   In this
        case, the client includes in the request only a URI reference to
        the document data (not the document data itself).

      - The Create-Job Request: A client that wants to submit a print
        job with multiple documents uses the Create-Job operation.  This
        operation is followed by an arbitrary number (one or more) of
        Send-Document and/or Send-URI operations (each creating another
        document for the newly create Job object).  The Send-Document
        operation includes the document data in the request (the client
        "pushes" the document data to the printer), and the Send-URI
        operation includes only a URI reference to the document data in
        the request (the Printer "pulls" the document data from the
        referenced location).  The last Send-Document or Send-URI
        request for a given Job object includes a "last-document"
        operation attribute set to 'true' indicating that this is the
        last request.

(https://tools.ietf.org/html/rfc3382)

### 7.1 Additional tags defined for representing a collection attribute
    value

   The 'collection' attribute syntax uses the tags defined in Table 3.

   Table 3 - Tags defined for encoding the 'collection' attribute syntax

        Tag name         Tag
                         value     Meaning

        begCollection    0x34      Begin the collection attribute value.

        endCollection    0x37      End the collection attribute value.

        memberAttrName   0x4A      The value is the name of the
                                   collection member attribute

RFC 3382   IPP: The 'collection' attribute syntax   September 2002[Page 14]

   Additional examples have been included in the appendices.

   The overall structure of the two collection values can be pictorially
   represented as:

      "media-col" =
        {  "media-color" =  'blue';
           "media-size" =
           {    "x-dimension" = 6;
                "y-dimension" = 4
             }
        },

   The full encoding is in table 5.  A simplified view of the encoding
   looks like this:

           Table 4 - Overview Encoding of "media-col" collection

      Tag Value             Name                  Value

      begCollection         media-col             ""

      memberAttrName        ""                    media-color

      keyword               ""                    blue

      memberAttrName        ""                    media-size

      begCollection         ""                    ""

      memberAttrName        ""                    x-dimension

      integer               ""                    6

      memberAttrName        ""                    y-dimension

      integer               ""                    4

      endCollection         ""                    ""

      endCollection         ""                    ""










deBry, et. al.              Standards Track                    [Page 15]

RFC 3382         IPP: The 'collection' attribute syntax   September 2002


           Table 5 - Example Encoding of "media-col" collection

      Octets       Symbolic Value  Protocol   comments
                                   field

      0x34         begCollection   value-tag  beginning of the "media-
                                              col" collection attribute

      0x0009                       name-      length of (collection)
                                   length     attribute name

      media-col    media-col       name       name of (collection)
                                              attribute

      0x0000                       value-     defined to be 0 for this
                                   length     type

                                              no value (since value-
                                              length was 0)

      0x4A         memberAttrName  value-tag  starts a new member
                                              attribute: "media-color"

      0x0000                       name-      defined to be 0 for this
                                   length     type, so part of 1setOf

                                              no name (since name-length
                                              was 0)

      0x000B                       value-     length of "media-color"
                                   length     keyword

      media-color  media-color     value      value is name of 1st
                                              member attribute


      0x44         keyword type    value-tag  keyword type

      0x0000                       name-      0 indicates 1setOf
                                   length

                                              no name (since name-length
                                              was 0)

