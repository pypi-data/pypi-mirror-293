begin
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'SQLTERMINATOR', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'PRETTY', true);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'SEGMENT_ATTRIBUTES', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'STORAGE', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'CONSTRAINTS', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'REF_CONSTRAINTS', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'EMIT_SCHEMA', false);
        end;