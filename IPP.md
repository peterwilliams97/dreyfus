https://tools.ietf.org/html/draft-sweet-rfc2910bis-07

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


   http://tools.ietf.org/html/rfc2567#section-5.2

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
