% given a set of quality and similarity matrices, select the k best
% sentences from each document

n_selections = 100;

qual = load('qual.mat', '-mat');
sim = load('sim.mat', '-mat');

sim_field_order = cell(size(fieldnames(sim)));
qual_field_order = cell(size(fieldnames(sim)));

for i = 1 : length(fieldnames(qual))
    sim_field_order{i} = char(join(["s", string(i-1)], ""));
    qual_field_order{i} = char(join(["q", string(i-1)], ""));
end

qual = orderfields(qual, qual_field_order);
qual_fields = fieldnames(qual);

sim = orderfields(sim, sim_field_order);
sim_fields = fieldnames(sim);

%selections = [];
selections = zeros(length(qual_fields),n_selections);

for curr_doc = 1 : length(qual_fields)
    
    qual_mat = qual.(char(qual_fields(curr_doc)));
    sim_mat = sim.(char(sim_fields(curr_doc)));
    
    l_ensemble = sim_mat .* (qual_mat*qual_mat');       
    l_ensemble = 0.5*(l_ensemble+l_ensemble');
    [v, lam] = eig(full(l_ensemble));
    lam(lam<0) = 0;
    l_ensemble = v*lam*v';

    candidates = true(length(qual_mat),1);

    %selections = horzcat(selections, zeros(n_selections,1));
    val_old = 0;

    for t = 1 : min(n_selections, length(qual_mat))
        inds = find(candidates);
        p = zeros(size(inds));
        
        for iter = 1 : length(inds)
            i = inds(iter);
            %curr_selections_tmp = selections(1:t,curr_doc);
            curr_selections_tmp = selections(curr_doc,1:t);
            curr_selections_tmp(t) = i;
            p(iter) = (det(l_ensemble(curr_selections_tmp,curr_selections_tmp)) - val_old);
        end
        
        [val, pos] = max(p);
        %selections(t,curr_doc) = inds(pos);
        selections(curr_doc,t) = inds(pos);
        %val_old = det(l_ensemble(selections(1:t,curr_doc),selections(1:t,curr_doc)));
        val_old = det(l_ensemble(selections(curr_doc,1:t),selections(curr_doc,1:t)));
        %candidates(selections(1:t,curr_doc)) = false;
        candidates(selections(curr_doc,1:t)) = false;
    end
end

%selections = selections';
save('sel.mat','selections');