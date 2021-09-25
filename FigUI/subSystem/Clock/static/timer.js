$(function() {

    var gate = $(window),
    cog = $('.rotator'),
    field = $('#result'),
    zone = cog.width(),
    slot = cog.height()/2,
    base = 1.5*slot,
    list = [],
    niche = [0,0,0],
    term = 100, // duration of full animation cycle will be discounted with dragging distance
    up = true,
    yaw = 'mousemove.ambit touchmove.ambit',
    hike = 'mouseup.turf touchend.turf';
    
    pulseMuzzle();
    tallyCells();
    
    if (document.readyState == 'complete') interAction();
    else gate.one('load', interAction);
    
    gate.on('mouseleave touchcancel', function(e) {
    
        !(e.type == 'mouseleave' && e.relatedTarget) && lotRelease(true);
    });
    
    function interAction() {
    
    niche.length = cog.length;
    
    cog.scrollTop(base).each(function(unit) {
    
        var pinion = $(this),
        digit = pinion.find('.quota'),
        item = digit.parent(),
        cipher = Number(niche[unit])%60 || 0;
        list[unit] = digit;
        niche[unit] = 0;
        // field.append(0);
        field.text("00:00:00s");
    
        for (var i = 0; i < cipher; i++) nextNumber(pinion, unit, item, true);
    
        pinion.mousewheel(function(turn, delta) {
    
            if (isBusy(pinion)) return false;
    
            up = delta > 0;
            nextNumber(pinion, unit, item);
    
            return false;
        });
    
        digit.on('mousedown touchstart', function(e) {
    
            if (e.which && e.which != 1 || isBusy(pinion)) return false;
    
            var ken = {}, zest = $(this);
    
            tagPoints(zest, e, ken);
    
            zest.on(hike, function() {
    
                wipeSlate(zest);
    
                if (ken.hit || ken.core) return;
    
                lotRelease();
                up = ken.spot == 1;
                nextNumber(pinion, unit, item, ken.cap);
            });
    
            gate.on(yaw, function(e) {
    
                hubTrace(e, ken);
            })
            .on(yaw, $.restrain(40, function() {
    
                shapeShift(item, ken.cap);
                up = ken.cap < 0;
    
                if (ken.jot != slot) return;
    
                lotRelease(false, zest);
                nextNumber(pinion, unit, item, true);
            }))
            .on(hike, function() {
    
                lotRelease(false, zest);
                nextNumber(pinion, unit, item, ken.cap, !ken.hit);
            });
    
            return false;
        });
    
    }).fadeTo(0,1);
    
    function tagPoints(mean, task, bit) {
    
        var nod = task.originalEvent.touches,
        weigh = mean.offset();
    
        bit.loom = nod ? nod[0].pageX : task.pageX;
        bit.rise = nod ? nod[0].pageY : task.pageY;
        bit.mark = bit.rise-weigh.top;
        bit.note = bit.loom-weigh.left;
        bit.spot = mean.index();
        bit.core = bit.spot == 2;
        bit.idea = mean;
    }
    
    function hubTrace(act, gob) {
    
        var peg = act.originalEvent.touches,
        due = peg ? peg[0].pageX : act.pageX,
        fly = peg ? peg[0].pageY : act.pageY;
    
        gob.cap = Math.max(-slot, Math.min(fly-gob.rise, slot));
        gob.jot = Math.abs(gob.cap);
        gob.hit = gob.jot > 30;
    
        if (gob.core || gob.nix) return;
    
        var way = gob.note-gob.loom+due,
        brim = way < 0 || way > zone,
        edge = gob.mark+gob.cap-slot/2;
    
        if (gob.spot == 1) {
        var out = slot-gob.mark < gob.cap;
        gob.nix = out || brim || edge < 0;
        }
        else {
        out = gob.mark < -gob.cap;
        gob.nix = out || brim || edge > 0;
        }
    
        gob.nix && wipeSlate(gob.idea);
    }
    
    function wipeSlate(topic) {
    
        topic.off(hike);
    }
    
    function isBusy(whirl) {
    
        return whirl.is(':animated');
    }
    
    function nextNumber(aim, knob, wrap, quick, drop) {
    
        var hook = list[knob],
        zap = quick && typeof quick === 'boolean',
        intent = base;
    
        wrap.attr('style') && wrap.attr('style', '');
    
        if (quick && !zap) {
        var jump = Math.abs(quick);
        if (drop) var lapse = 2*jump/slot*term;
        else lapse = (slot-jump)/slot*term;
        aim.scrollTop(base-quick);
        }
        else if (!quick) lapse = term;
    
        if (!drop) up ? intent += slot : intent -= slot;
    
        if (zap) {
        aim.scrollTop(intent);
        revolveTooth();
        }
        else aim.animate({scrollTop: intent}, lapse, revolveTooth);
    
    function revolveTooth() {
    
        if (drop) return;
    
        up ? hook.eq(0).appendTo(wrap) : hook.eq(9).prependTo(wrap);
    
        list[knob] = wrap.find('.quota');
        niche[knob] = Number(list[knob].eq(2).text());
    
        aim.scrollTop(base);
        var Niche = Array();
        for (var i=0; i<3; i++) {
            ele = niche[i].toString().padStart(2, '0');;
            Niche.push(ele);
        } 
        field.text(Niche.join(':')+"s");
    }
    }
    }
    
    function shapeShift(goal, ardor) {
    
        var pith = 'translateY(' + ardor + 'px)';
    
        goal.css({'-ms-transform': pith, '-webkit-transform': pith, transform: pith});
    }
    
    function lotRelease(broad, heart) {
    
        if (broad) var plan = '.quota';
        else plan = heart || '';
    
        gate.off(yaw).add(plan).off(hike);
        broad && cog.find('>').attr('style', '');
    }
    
    function tallyCells() {
    
        cog.each(function() {
        const K = 60;
            for (var i = 0; i < K; i++) {
    
            // var n; !i ? n = 8 : (i == 1 ? n = 9 : n = i-2);
        var n = (i+K-2)%(K);
            $(this).append('<div></div>').find('div').eq(i).text(n).addClass('quota');
    
            if (i == K-1) $(this).children().wrapAll('<div></div>');
            }
        });
    }
    
    function pulseMuzzle() {
    
        $.restrain = function(delay, callback, hind) {
    
            var executed = 0, debounce,
            throttle = function() {
    
            var elapsed = Math.min(delay, Date.now()-executed),
            remain = delay-elapsed;
            debounce && clearTimeout(debounce);
            elapsed == delay && runIt();
            if (hind && remain) debounce = setTimeout(runIt, remain);
    
            function runIt() {
            executed = Date.now();
            callback.apply(this, arguments);
            }
            }
            return throttle;
        }
    }
    });