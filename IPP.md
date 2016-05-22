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
