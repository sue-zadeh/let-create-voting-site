# TO USE confirm_dialog.js, DO THE FOLLOWING FOUR STEPS: 
1. In the html file, if the following code is not there, add it,
it should only be present in the file once even if you want
multiple confirm dialogs:

```
<!-- Static Backdrop Modal -->
<div class="modal fade vms-modal-dialog" id="vms-dialog" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
aria-labelledby="vmsDialogLabel" aria-hidden="true">
  <div class="modal-dialog">
      <div class="modal-content">
          <div class="modal-header">
              <h1 class="modal-title fs-5" id="vmsDialogLabel">Approve?</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
              <p class="modal-body-description"></p>
              <textarea
                class="form-control modal-text-area"
                rows="3"
                required
              ></textarea>
              <p class="vms-modal-validation" style="color: red;"></p>
          </div>
          <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-success vms-confirm-button">Yes</button>
          </div>
      </div>
  </div>
</div>
```

2. On the button that shows the confirm dialog,
paste the following and change the
data-vms-* attributes to your usage:

```
<a class="btn btn-success" href="#" data-bs-toggle="modal"
            data-bs-target="#vms-dialog"
            data-vms-modal-title="Deny"
            data-vms-action-text="Deny"
            data-vms-modal-body="Are you sure you want to deny this appeal? Please provide a reason for this:"
            data-vms-modal-need-reason="yes"
            data-vms-url-id="{{appeal['appeal_id']}}"
            data-vms-url="{{url_for('deny_appeal')}}"
            >Deny</a>

```
3. Put the following at the bottom of the html file if it's not
already there.

```
<script src="{{ url_for('static', filename='js/confirm_dialog.js') }}"></script>  
// Put it just before the final {%endblock%}
```

4. In the route handler, the id and textarea reason can be accessed
via request.json['id_data'] and request.json['reason'] respectively

e.g.

```
@app.route("/deny_appeal", methods=['PUT'])
def deny_appeal():
    role, site_role = user_role()
    if site_role != 'site admin':
        return
    try:
        cursor = VmsCursor()
        cursor.execute("""UPDATE site_wide_ban_appeals
                    SET response = %s, status = 'denied', response_date = %s
                    WHERE appeal_id = %s""",
                        (request.json['reason'], datetime.now(), int(request.json['id_data'])))
    except:
        flash("Deny user's appeal failed.", "danger")
    else:
        flash("User's appeal has been denied.", 'success')
    return ''
```
